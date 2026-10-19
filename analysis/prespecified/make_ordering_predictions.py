"""Write prespecified ordering-test predictions before any ordering_test_* simulation runs."""
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from insurance_sim.diagnostics import balanced_small_noise_coefficient
from insurance_sim.model import slopes_for_mode

REFERENCE = Path("analysis/reports/fig7_mechanism_reversal_summary.csv")
OUT = Path("analysis/prespecified/ordering_predictions_2026-10-19.json")

ref = pd.read_csv(REFERENCE)
ref["x"] = ref.small_noise_coefficient * ref.sigma_env**2
ref = ref[ref.floor_replicate_max == 0]
curves = {}
for S, g in ref.groupby("n_species"):
    g = g.groupby("x", as_index=False)["cv2_ratio"].mean().sort_values("x")
    curves[int(S)] = (np.log(g.x.to_numpy()), np.log(g.cv2_ratio.to_numpy()))


def interp(S: int, x: float) -> float | None:
    lx, lr = curves[S]
    if not lx[0] <= np.log(x) <= lx[-1]:
        return None
    return float(np.exp(np.interp(np.log(x), lx, lr)))


cells = []
for alpha in (0.2, 0.45):
    for S in (4, 8, 12):
        for phi in (0.2, 0.6):
            c = balanced_small_noise_coefficient(
                response_slopes=slopes_for_mode("mixed", S), alpha_intra=1.0, alpha_inter=alpha, phi=phi
            )
            for sigma in (0.2, 0.35, 0.5, 0.7, 1.0):
                x = c * sigma**2
                cell = {"alpha_inter": alpha, "S": S, "phi": phi, "sigma_env": sigma,
                        "c": round(c, 6), "x": round(x, 6)}
                if S in (4, 8):
                    pred = interp(S, x)
                    cell["R_pred"] = None if pred is None else round(pred, 5)
                    if S == 8 and pred is not None:
                        cell["reversal_call"] = (
                            "reversal" if pred > 1.05 else "no_reversal" if pred < 0.95 else "too_close"
                        )
                else:
                    ref8 = interp(8, x)
                    cell["R_ref_S8"] = None if ref8 is None else round(ref8, 5)
                cells.append(cell)

doc = {
    "written_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "reference_curve": {
        "source": str(REFERENCE),
        "cells": "floor-free cells (floor_replicate_max == 0) of the three sigma_mechanism grids, by richness",
        "method": "linear interpolation of log R on log x, x = c * sigma_env^2; no extrapolation beyond the reference x-range",
    },
    "criteria": {
        "C1_accuracy": "Among S = 4 and S = 8 cells with a prediction and no retained floor contact at either endpoint, at least 90% have |R_obs / R_pred - 1| <= 0.10. Basis: leave-one-out interpolation error in the reference cells was at most 7.3% (S = 4) and 4.2% (S = 8).",
        "C2_reversal_call": "Every S = 8 cell with a call of reversal or no_reversal and no retained floor contact has its observed R on the predicted side of one. Calls are reversal if R_pred > 1.05, no_reversal if R_pred < 0.95, otherwise too_close (not scored).",
        "C3_richness_direction": "Among S = 12 cells with an S = 8 reference value and no retained floor contact, at least 80% have R_obs > R_ref_S8, i.e. richer communities sit above the eight-species curve at the same x.",
        "reporting": "All cells are reported, including floor-contact and out-of-range cells. A failed criterion is reported as a failure and narrows the claim; there is no parameter expansion.",
    },
    "cells": cells,
}
OUT.write_text(json.dumps(doc, indent=1) + "\n")
n_pred = sum(1 for c in cells if c.get("R_pred") is not None)
calls = [c.get("reversal_call") for c in cells if c.get("reversal_call")]
print(f"wrote {OUT}: {len(cells)} cells, {n_pred} S4/S8 predictions, calls {pd.Series(calls).value_counts().to_dict()}, S12 refs {sum(1 for c in cells if c.get('R_ref_S8') is not None)}")
