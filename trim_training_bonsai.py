"""
Trims Training and Week 3 Retraining Bonsai CSVs to the first 5 hours.
Overwrites files in place. Run once before committing to GitHub.
"""
import os, glob
import pandas as pd

KEEP_HOURS = 5
KEEP_S     = KEEP_HOURS * 3600

BASE = os.path.dirname(os.path.abspath(__file__))
FOLDERS = [
    os.path.join(BASE, 'Data', 'Cued photometry', 'Raw', 'Bonsai Data', 'Training'),
    os.path.join(BASE, 'Data', 'Cued photometry', 'Raw', 'Bonsai Data', 'Week 3 Retraining'),
]

files = []
for folder in FOLDERS:
    files.extend(glob.glob(os.path.join(folder, '**', '*.csv'), recursive=True))

print(f'Found {len(files)} files to trim.\n')

for path in sorted(files):
    size_mb_before = os.path.getsize(path) / 1e6
    df = pd.read_csv(path, header=0)
    t  = df.iloc[:, 0]
    cutoff = t.min() + KEEP_S
    df_trim = df[t <= cutoff]
    dur_h = (t.max() - t.min()) / 3600
    rows_before = len(df)
    rows_after  = len(df_trim)
    df_trim.to_csv(path, index=False)
    size_mb_after = os.path.getsize(path) / 1e6
    name = os.path.relpath(path, BASE)
    print(f'  {os.path.basename(path)}')
    print(f'    {dur_h:.1f}h  {rows_before:,} rows  {size_mb_before:.0f}MB  →  {rows_after:,} rows  {size_mb_after:.0f}MB')

print(f'\nDone. All files trimmed to first {KEEP_HOURS} hours.')
