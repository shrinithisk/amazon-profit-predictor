"""
Amazon ML Model Trainer (Helium 10 Grade)
Loads generated products.csv, prepares features, and trains two models:
1. Sales Estimator (Regressor) - to predict monthly sales units.
2. Profitability Classifier (Classifier) - to predict if product is a high-value winner.
Saves models and scaling files.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
import pickle

# Category mapping to ensure consistent encoding
CATEGORY_MAPPING = {
    'Consumer Electronics': 0,
    'Home & Kitchen': 1,
    'Apparel & Fashion': 2,
    'Beauty & Personal Care': 3,
    'Sports & Fitness': 4,
    'Toys & Games': 5
}

def train_models():
    print("📖 Loading products.csv...")
    df = pd.read_csv('products.csv')
    
    # Map category strings to integers
    df['category_encoded'] = df['category'].map(CATEGORY_MAPPING)
    
    # Features list (same for both models)
    features = ['category_encoded', 'price', 'cost', 'rating', 'num_reviews', 'competition', 'listing_score']
    
    # Check for NaN values just in case
    df = df.dropna(subset=features + ['monthly_sales', 'is_profitable'])
    
    X = df[features]
    y_sales = df['monthly_sales']
    y_class = df['is_profitable']
    
    # Split data (80% train, 20% test)
    X_train, X_test, y_sales_train, y_sales_test, y_class_train, y_class_test = train_test_split(
        X, y_sales, y_class, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("\n" + "="*50)
    print("🤖 TRAINING SALES ESTIMATOR (REGRESSOR)")
    print("="*50)
    
    sales_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=8)
    sales_model.fit(X_train_scaled, y_sales_train)
    
    # Evaluate sales estimator
    sales_pred = sales_model.predict(X_test_scaled)
    mae = mean_absolute_error(y_sales_test, sales_pred)
    r2 = r2_score(y_sales_test, sales_pred)
    
    print(f"Sales Estimator Trained.")
    print(f"Mean Absolute Error: {mae:.2f} units")
    print(f"R² Score (Variance explained): {r2*100:.1f}%")
    
    print("\n" + "="*50)
    print("🤖 TRAINING PROFITABILITY PREDICTOR (CLASSIFIER)")
    print("="*50)
    
    class_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=6)
    class_model.fit(X_train_scaled, y_class_train)
    
    # Evaluate classifier
    class_pred = class_model.predict(X_test_scaled)
    acc = accuracy_score(y_class_test, class_pred)
    
    print(f"Profitability Classifier Trained.")
    print(f"Accuracy: {acc*100:.1f}%")
    
    # Save objects
    print("\n" + "="*50)
    print("💾 SAVING ML PIPELINE COMPONENTS")
    print("="*50)
    
    pickle.dump(sales_model, open('sales_model.pkl', 'wb'))
    pickle.dump(class_model, open('classifier_model.pkl', 'wb'))
    pickle.dump(scaler, open('scaler.pkl', 'wb'))
    
    print("✅ Saved 'sales_model.pkl'")
    print("✅ Saved 'classifier_model.pkl'")
    print("✅ Saved 'scaler.pkl'")
    print("🎉 ML training pipeline completed successfully!")

if __name__ == "__main__":
    train_models()
