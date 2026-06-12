import pickle
import numpy as np
import pandas as pd

try:
    with open('d:/Rera_Scraping_March_25/Suraj/Cancer_deductoin_project/XGBoost.pkl', 'rb') as f:
        model = pickle.load(f)
    
    estimator = model.best_estimator_
    importances = estimator.feature_importances_
    feature_names = model.feature_names_in_
    
    indices = np.argsort(importances)[::-1]
    
    print("Top 15 features:")
    top_15 = []
    for i in range(15):
        top_15.append(feature_names[indices[i]])
        print(f"{i+1}. {feature_names[indices[i]]}: {importances[indices[i]]}")
        
    print("\nTop 15 Feature list for copy-paste:")
    print(top_15)

except Exception as e:
    print("Error:", e)
