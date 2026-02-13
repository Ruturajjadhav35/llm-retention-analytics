import pandas as pd

print("Checking column names in all result files...")
print()

files = {
    'user_segments':      'results/user_segments.csv',
    'event_types':        'results/event_types.csv',
    'feature_adoption':   'results/feature_adoption.csv',
    'retention_segment':  'results/retention_by_segment.csv',
    'conversion_rate':    'results/conversion_rate.csv',
}

for name, path in files.items():
    df = pd.read_csv(path)
    print(f"📄 {name}:")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Shape:   {df.shape}")
    print()