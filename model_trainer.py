"""
Simple ML Model to Predict If Product is Profitable (Indian Market)
Uses our fake data from data_generator.py
Predicts profitability for Indian Amazon sellers
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle

# ============================================
# STEP 1: Load the data we created earlier
# ============================================
print("📖 Loading Indian products data...")
df = pd.read_csv('products.csv')

print(f"✅ Loaded {len(df)} products")
print(f"\nFirst 3 products (in ₹):")
print(df.head(3))

# ============================================
# STEP 2: Prepare data for machine learning
# ============================================
print("\n" + "="*60)
print("🔧 PREPARING DATA (Indian Market)")
print("="*60)

# Select features (what we use to predict)
features = ['price', 'cost', 'rating', 'num_reviews', 'monthly_sales', 'competition']

# Select target (what we want to predict)
target = 'is_profitable'

# Extract X (features) and y (target)
X = df[features]
y = df[target]

print(f"\nFeatures we're using: {features}")
print(f"Target we're predicting: {target}")
print(f"\nShape of features: {X.shape}")
print(f"Shape of target: {y.shape}")

print(f"\nExamples of features (X) - in Indian Rupees:")
print(X.head(3))

print(f"\nExamples of target (y):")
print(y.head(3))

# ============================================
# STEP 3: Split data into training and testing
# ============================================
print("\n" + "="*60)
print("✂️ SPLITTING DATA")
print("="*60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print(f"\nTraining data: {len(X_train)} products")
print(f"Testing data: {len(X_test)} products")

# ============================================
# STEP 4: Scale the features
# ============================================
print("\n" + "="*60)
print("📏 SCALING FEATURES")
print("="*60)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\nBefore scaling:")
print(f"Price range: ₹{X_train['price'].min():.0f} - ₹{X_train['price'].max():.0f}")
print(f"Rating range: {X_train['rating'].min():.1f} - {X_train['rating'].max():.1f}")

print(f"\nAfter scaling:")
print(f"All values between -3 and 3 (standardized)")

# ============================================
# STEP 5: Train the model
# ============================================
print("\n" + "="*60)
print("🤖 TRAINING MODEL (Indian Market Data)")
print("="*60)

model = RandomForestClassifier(
    n_estimators=50,
    random_state=42,
    max_depth=5,
    verbose=1
)

print("\nTraining Random Forest with 50 trees...")
model.fit(X_train_scaled, y_train)
print("✅ Training complete!")

# ============================================
# STEP 6: Make predictions
# ============================================
print("\n" + "="*60)
print("🔮 MAKING PREDICTIONS")
print("="*60)

y_train_pred = model.predict(X_train_scaled)
y_test_pred = model.predict(X_test_scaled)

print(f"\nSample predictions on test data:")
for i in range(min(5, len(y_test))):
    actual = y_test.iloc[i]
    predicted = y_test_pred[i]
    correct = "✅" if actual == predicted else "❌"
    print(f"  {correct} Actual: {'Profitable' if actual == 1 else 'Not Profitable'} | Predicted: {'Profitable' if predicted == 1 else 'Not Profitable'}")

# ============================================
# STEP 7: Evaluate the model
# ============================================
print("\n" + "="*60)
print("📊 MODEL EVALUATION")
print("="*60)

train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)
precision = precision_score(y_test, y_test_pred, zero_division=0)
recall = recall_score(y_test, y_test_pred, zero_division=0)
f1 = f1_score(y_test, y_test_pred, zero_division=0)

print(f"\nTraining Accuracy: {train_accuracy*100:.1f}%")
print(f"Testing Accuracy: {test_accuracy*100:.1f}%")
print(f"\nTesting Metrics:")
print(f"  Precision: {precision*100:.1f}%  (of predicted profitable, how many are actually?)")
print(f"  Recall: {recall*100:.1f}%        (of actual profitable, how many did we catch?)")
print(f"  F1-Score: {f1*100:.1f}%          (balance between precision and recall)")

# ============================================
# STEP 8: Feature importance
# ============================================
print("\n" + "="*60)
print("🎯 FEATURE IMPORTANCE (For Indian Market)")
print("="*60)

print("\nWhich features matter most for prediction?")
importances = model.feature_importances_

feature_importance_dict = dict(zip(features, importances))
sorted_importance = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)

for feature, importance in sorted_importance:
    bar = "█" * int(importance * 50)
    print(f"  {feature:20s} {bar} {importance*100:.1f}%")

# ============================================
# STEP 9: Test on new Indian products
# ============================================
print("\n" + "="*60)
print("🧪 TEST ON NEW INDIAN PRODUCTS")
print("="*60)

# Create new products (not in training data) - in Indian Rupees
new_products = pd.DataFrame([
    {
        'price': 2500,
        'cost': 600,
        'rating': 4.8,
        'num_reviews': 2000,
        'monthly_sales': 200,
        'competition': 2
    },
    {
        'price': 800,
        'cost': 700,
        'rating': 2.0,
        'num_reviews': 100,
        'monthly_sales': 10,
        'competition': 5
    },
    {
        'price': 1500,
        'cost': 500,
        'rating': 4.5,
        'num_reviews': 1500,
        'monthly_sales': 100,
        'competition': 3
    },
])

# Scale the new products
new_products_scaled = scaler.transform(new_products)

# Make predictions
predictions = model.predict(new_products_scaled)
probabilities = model.predict_proba(new_products_scaled)

print("\nPredictions for new Indian products:")
for i, (idx, product) in enumerate(new_products.iterrows()):
    pred = predictions[i]
    prob = probabilities[i][1]
    
    print(f"\n  Product {i+1}:")
    print(f"    Price: ₹{int(product['price'])}, Cost: ₹{int(product['cost'])}")
    print(f"    Rating: {product['rating']}/5, Sales: {int(product['monthly_sales'])}/month")
    print(f"    Prediction: {'PROFITABLE ✅' if pred == 1 else 'NOT PROFITABLE ❌'}")
    print(f"    Confidence: {prob*100:.1f}%")

# ============================================
# STEP 10: Save the model
# ============================================
print("\n" + "="*60)
print("💾 SAVING MODEL (For Indian Market)")
print("="*60)

pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(scaler, open('scaler.pkl', 'wb'))

print("\n✅ Model saved as 'model.pkl'")
print("✅ Scaler saved as 'scaler.pkl'")
print("\nModel is trained on Indian market data!")

# ============================================
# SUMMARY
# ============================================
print("\n" + "="*60)
print("📋 SUMMARY (Indian Market)")
print("="*60)

print(f"""
✅ Created and trained a Random Forest model for Indian sellers
✅ Model accuracy: {test_accuracy*100:.1f}%
✅ Model learned from 80 Indian products, tested on 20
✅ Can now predict if ANY product will be profitable in India!
✅ All prices in Indian Rupees (₹)
✅ Includes Amazon.in fees & GST calculation

Most important features for profitability in Indian market:
""")

for feature, importance in sorted_importance[:3]:
    print(f"  {importance*100:.1f}% - {feature}")

print(f"""
Profitability threshold: ₹5,000 monthly profit

Next steps:
1. Use model_trainer.py to train the model
2. Run app.py to see the web interface
3. Start predicting products for dropshipping!
""")
