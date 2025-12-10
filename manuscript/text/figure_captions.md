# Figure captions (draft)

1. **Figure 1 – Insurance patterns under mixed vs aligned responses** (`manuscript_panels.png` / `.pdf`)
   - Panel A: Heatmap of community CV across σ_env (columns) and ρ_env (rows) for mixed slopes, S=4. Cooler colors indicate lower variability; CV declines with increasing ρ_env and σ_env effects are damped by compensation.
   - Panel B: Heatmap of community CV for positive slopes, S=4. Variability increases with ρ_env, showing loss of insurance when responses are aligned.
   - Panel C: CV vs ρ_env lines at σ_env=0.5 for S=4 and S=8, contrasting mixed (solid) vs positive (dashed) slopes. Mixed lines slope downward; positive lines upward, with richness reducing amplitude.
   - Panel D: Imposed vs realised growth synchrony (mean pairwise correlation). Mixed responses sit below the 1:1 line (realised < imposed), positive responses above it.

2. **Figure 2 – Imposed vs realised synchrony by slope mode** (`imposed_vs_realised_panels.png`)
   - Panel A: Realised mean growth correlations vs ρ_env for mixed slopes at σ_env=0.5, separated by richness. Curves fall below the 1:1 line, often becoming negative at high ρ_env.
   - Panel B: Realised mean growth correlations vs ρ_env for positive slopes at σ_env=0.5. Curves sit above the 1:1 line, showing strong response synchrony.
   - Panel C: Difference Δcorr = realised − ρ_env vs ρ_env for mixed and positive slopes, emphasising negative deltas for mixed and positive deltas for aligned responses.

3. **Figure 3 – CV vs synchrony metrics (mixed slopes)** (`cv_vs_synchrony_mixed.png`)
   - Panel A: Scatter of CV_total vs φ_LdM across scenarios in the mixed-slope grid. Lower φ_LdM is associated with lower CV_total, especially at higher richness.
   - Panel B: Scatter of CV_total vs mean pairwise growth correlation for the same scenarios, showing a similar negative association.

4. **Figure 4 – Richness effect on community CV** (`cv_richness_scaling_mixed.png`)
   - Panel A: Mean CV vs species richness averaged over ρ for each σ_env. CV drops steeply from S=2→4 and continues to S=8.
   - Panel B (if included): alternative richness slices or scenario subsets if needed.

5. **Figure 5 – Environmental persistence sensitivity** (`cv_phi_sensitivity_sigma0.5_extended.png`)
   - CV vs ρ_env at σ_env=0.5 for φ = 0, 0.4, 0.7, 0.9, 0.95 (S=2,4). Higher φ increases CV_total (partly via higher stationary environmental variance), but the qualitative insurance pattern (mixed vs positive contrast, richness effect) remains.

(Assets live under `analysis/reports/` and are mirrored to `manuscript/figures/` by `analysis/run_all.py`.) 
