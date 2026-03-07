from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_plot_grid_accepts_preview_schema_without_slope_mode(tmp_path: Path) -> None:
    df = pd.DataFrame(
        {
            "n_species": [2, 2],
            "sigma_env": [0.0, 0.5],
            "rho_env": [0.0, 0.5],
            "phi": [0.4, 0.4],
            "cv_total": [0.1, 0.2],
            "phi_ldm": [0.95, 0.75],
            "mean_pairwise_corr": [0.05, 0.35],
        }
    )
    input_path = tmp_path / "preview.parquet"
    out_prefix = tmp_path / "preview"
    df.to_parquet(input_path, index=False)

    subprocess.run(
        [
            sys.executable,
            "analysis/plot_grid.py",
            "--input",
            str(input_path),
            "--out-prefix",
            str(out_prefix),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    assert Path(f"{out_prefix}_summary.csv").exists()
    assert Path(f"{out_prefix}_cv.png").exists()
    assert Path(f"{out_prefix}_phi.png").exists()
