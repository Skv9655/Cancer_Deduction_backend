import pandas as pd
import json

try:
    df = pd.read_csv("C:/Users/Admin/Downloads/data.csv")
    # Drop non-feature columns
    if 'id' in df.columns:
        df = df.drop('id', axis=1)
    if 'diagnosis' in df.columns:
        df = df.drop('diagnosis', axis=1)
    # Also drop unnamed column if any
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    means = df.mean().to_dict()
    with open('feature_means.json', 'w') as f:
        json.dump(means, f, indent=4)
    print("Means saved successfully to feature_means.json")
except Exception as e:
    print("Error:", e)
