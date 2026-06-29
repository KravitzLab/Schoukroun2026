# Schoukroun2026

---

## Cued Photometry Notebooks

### [Preprocessing](https://colab.research.google.com/drive/11MCwOWZlziLwthGG0fjh_H5S5ix4sYVC?usp=sharing)

Downloads raw fluorescence recordings and Bonsai tracking files directly from this repository, processes each session, and uploads the results back to the `Processed/` folder.

**What it does, in order:**

1. **File validation** — checks that every expected raw file for each mouse is present and warns if anything is missing.

2. **Skip logic** — scans the `Processed/` folder on GitHub before doing any work. Sessions that already have a processed output are skipped, so the notebook is safe to re-run as new data is added.

3. **Signal processing** — for each RWD fluorescence recording:
   - Parses event timestamps from the `Events` column. A rising edge shorter than 0.3 s is classified as a tone onset; 0.3 s or longer is a pellet grab. Week 3 Tone Only sessions are parsed in tone-only mode (all events treated as tone onsets).
   - Fits and removes a double-exponential photobleach trend from both the 470 nm and 410 nm channels.
   - Regresses the 410 nm isosbestic channel against the 470 nm signal to remove motion artifacts.
   - Z-scores the corrected signal using the 25th percentile of the trace as the baseline distribution, preserving large reward-evoked peaks.

4. **Tracking QC** — generates a movement trace plot for each session using the Bonsai tracking file, overlaid with the FED device location and tone event times, so recording quality can be visually confirmed.

5. **Download** — packages all newly processed CSVs into a zip file for local download.

---

### [Analysis](https://colab.research.google.com/drive/1IVTMziNgtBNCSD1-Iish3sTO55gYrjVl?usp=sharing)

Downloads the processed photometry and Bonsai files from `Processed/` and runs the full group-level analysis.

**What it does, in order:**

1. **Peri-event time histograms (PETH)** — for each mouse and session, extracts a ±2 s window around every tone onset, baseline-corrects each trial to the pre-tone period, and interpolates to 81 time points. Trials are averaged per mouse, then averaged across mice within each diet group.

2. **Response quantification** — summarizes each mouse's tone response as the mean delta-Z in the 0–2 s post-tone window (area under the curve equivalent). These per-mouse values are used for all group statistics.

3. **Group comparisons** — plots mean PETH traces and bar graphs comparing HFD and Chow across all four sessions (W1B, W1T, W3T, W3TO), with individual mouse values overlaid.

4. **Session progression** — shows how each diet group's tone response evolves across the experiment, with lines connecting individual mice across sessions.

5. **Statistics** — runs a 2-way mixed ANOVA (Diet × Session) using sessions where both groups have complete data, followed by Bonferroni-corrected pairwise post-hoc tests within each diet and between diets at each session. The Week 3 Trained session is reported separately with per-mouse values since it was collected in phases.

6. **Behavioral analysis** — uses the Bonsai tracking data to compute approach latency (time from tone onset to first FED contact, capped at 60 s and plotted on a log scale) and movement traces, compared between diet groups and across sessions.

---

## Data structure

```
Data/
  Cued photometry/
    Raw/
      RWD Data/          # raw fluorescence CSVs from the RWD system
      Bonsai Data/       # position tracking and event CSVs from Bonsai
    Processed/
      RWD Data/          # z-scored photometry output (written by Preprocessing)
      Bonsai Data/       # scaled tracking output (written by Preprocessing)
```

## Mice

| Cohort | Diet | Mice |
|--------|------|------|
| C21 | HFD | M1R, M3L, M4LL *(M2RR excluded — lost fiber)* |
| C55 | HFD | M1R, M2L, M3RR, M5RL |
| C30 | Chow | M1R, M2L, M3RR |
| C54 | Chow | M2L, M3RR, M4LL, M5RL |

Sessions: **W1B** = Week 1 Baseline, **W1T** = Week 1 Trained, **W3T** = Week 3 Trained, **W3TO** = Week 3 Tone Only.
