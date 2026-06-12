import pandas as pd
import json

top_15 = ['perimeter_worst', 'perimeter_mean', 'radius_worst', 'concave points_mean', 'concave points_worst', 'radius_mean', 'texture_worst', 'area_worst', 'area_mean', 'concavity_worst', 'compactness_worst', 'smoothness_worst', 'compactness_se', 'area_se', 'texture_mean']

try:
    df = pd.read_csv("C:/Users/Admin/Downloads/data.csv")
    ranges = {}
    for feature in top_15:
        # Some fields might have spaces in data but underscores in our code.
        # But wait, df has the exact same names as top_15 (with spaces).
        col = feature
        if col in df.columns:
            ranges[col] = {
                "min": round(float(df[col].min()), 4),
                "max": round(float(df[col].max()), 4)
            }
        else:
            print(f"Warning: {col} not found in dataset")

    with open('feature_ranges.json', 'w') as f:
        json.dump(ranges, f, indent=4)
    print("Ranges saved successfully to feature_ranges.json")
except Exception as e:
    print("Error:", e)
