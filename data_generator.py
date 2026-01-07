"""
Simple Amazon Product Data Generator (For India)
Generates 100 fake Amazon products for Indian sellers
Uses Indian Rupees (₹) and Indian market patterns
"""

import pandas as pd
import numpy as np
import random

# Set seed so we get same data every time
np.random.seed(42)
random.seed(42)

# ============================================
# STEP 1: Define Product Categories (India)
# ============================================
# Adjusted for Indian market prices
categories = {
    'Electronics': {
        'avg_price': 2500,      # ₹2500 average
        'avg_cost': 800,        # ₹800 average cost
    },
    'Home & Kitchen': {
        'avg_price': 1500,      # ₹1500
        'avg_cost': 500,        # ₹500
    },
    'Clothing': {
        'avg_price': 800,       # ₹800
        'avg_cost': 250,        # ₹250
    },
    'Books': {
        'avg_price': 300,       # ₹300
        'avg_cost': 100,        # ₹100
    },
}

# Simple product names (in Hindi & English mix - common in India)
product_names = [
    'USB Hub', 'Mobile Charger', 'Mouse', 'Keyboard', 'Speaker',
    'Mixer Grinder', 'Coffee Maker', 'Cookware Set', 'Storage Box',
    'T-Shirt', 'Jeans', 'Hoodie', 'Jacket', 'Shoes',
    'Novel', 'Self-Help', 'Cookbook', 'Biography',
]

# ============================================
# STEP 2: Function to Generate ONE Product
# ============================================
def generate_one_product():
    """
    Create ONE fake Amazon product for Indian market
    Returns a dictionary with product info in Indian Rupees
    """
    
    # Pick random category
    category = random.choice(list(categories.keys()))
    cat_data = categories[category]
    
    # Pick random product name
    product_name = random.choice(product_names)
    
    # Generate price (varies around average, Indian prices)
    price = np.random.normal(
        loc=cat_data['avg_price'],           # Center around average
        scale=cat_data['avg_price'] * 0.2    # Vary by 20%
    )
    price = max(price, cat_data['avg_price'] * 0.5)  # Never too low
    price = round(price, 0)  # Round to nearest rupee (no decimals in India)
    
    # Generate cost (30-60% of price)
    cost_percent = np.random.uniform(0.3, 0.6)
    cost = price * cost_percent
    cost = round(cost, 0)
    
    # Generate rating (4.0 to 4.8 usually, sometimes low)
    if random.random() < 0.8:  # 80% have high rating
        rating = np.random.normal(4.5, 0.3)
    else:  # 20% have low rating
        rating = np.random.normal(2.5, 0.5)
    rating = np.clip(rating, 1.0, 5.0)
    rating = round(rating, 1)
    
    # Generate number of reviews
    num_reviews = int(np.random.uniform(100, 5000))
    
    # Generate monthly sales
    monthly_sales = int(np.random.uniform(10, 500))
    
    # Generate competition level (1-5)
    competition = random.randint(1, 5)
    
    # Calculate profit (Indian market fees)
    # Amazon.in takes approximately 30-40% commission (varies by category)
    amazon_fee_percent = np.random.uniform(0.30, 0.40)
    amazon_fee = price * amazon_fee_percent
    
    # GST (18% in India for most products)
    gst = price * 0.18
    
    # Total costs (cost + amazon fee + gst)
    total_cost = cost + amazon_fee + gst
    
    profit_per_unit = price - total_cost
    monthly_profit = profit_per_unit * monthly_sales
    
    # Is it profitable? (If makes more than ₹5000/month)
    is_profitable = 1 if monthly_profit > 5000 else 0
    
    # Return as dictionary
    return {
        'product_name': product_name,
        'category': category,
        'price': int(price),
        'cost': int(cost),
        'rating': rating,
        'num_reviews': num_reviews,
        'monthly_sales': monthly_sales,
        'competition': competition,
        'monthly_profit': round(monthly_profit, 0),
        'is_profitable': is_profitable,
    }

# ============================================
# STEP 3: Function to Generate MANY Products
# ============================================
def generate_dataset(num_products=100):
    """
    Generate multiple products and return as table
    
    Example:
    >>> df = generate_dataset(100)
    >>> print(df)  # Shows table with 100 rows
    """
    
    products = []
    
    # Generate each product
    for i in range(num_products):
        product = generate_one_product()
        products.append(product)
        
        # Print progress every 20 products
        if (i + 1) % 20 == 0:
            print(f"Generated {i + 1}/{num_products} products...")
    
    # Convert to table (pandas DataFrame)
    df = pd.DataFrame(products)
    
    print(f"\n✅ Generated {num_products} products!")
    return df

# ============================================
# STEP 4: Test it!
# ============================================
if __name__ == "__main__":
    
    print("🚀 Creating 100 fake Amazon India products...\n")
    
    # Generate dataset
    df = generate_dataset(num_products=100)
    
    # Show statistics
    print("\n" + "="*60)
    print("📊 DATASET STATISTICS (Indian Market)")
    print("="*60)
    print(f"\nTotal products: {len(df)}")
    print(f"Categories: {df['category'].nunique()}")
    print(f"\nAverage price: ₹{df['price'].mean():.0f}")
    print(f"Average cost: ₹{df['cost'].mean():.0f}")
    print(f"Average rating: {df['rating'].mean():.1f}/5")
    print(f"Average monthly sales: {df['monthly_sales'].mean():.0f} units")
    print(f"Average monthly profit: ₹{df['monthly_profit'].mean():.0f}")
    
    print(f"\nProfitable products: {df['is_profitable'].sum()} out of {len(df)}")
    print(f"Profitability rate: {df['is_profitable'].mean()*100:.1f}%")
    
    # Show first 5 products
    print("\n" + "="*60)
    print("🎁 FIRST 5 PRODUCTS (in Indian Rupees)")
    print("="*60)
    print(df.head())
    
    # Show one detailed product
    print("\n" + "="*60)
    print("📦 EXAMPLE PRODUCT (Detailed)")
    print("="*60)
    example = df.iloc[0]
    print(f"Name: {example['product_name']}")
    print(f"Category: {example['category']}")
    print(f"Selling Price: ₹{int(example['price'])}")
    print(f"Product Cost: ₹{int(example['cost'])}")
    print(f"Rating: {example['rating']}/5 ({int(example['num_reviews'])} reviews)")
    print(f"Monthly Sales: {int(example['monthly_sales'])} units")
    print(f"Competition: {int(example['competition'])}/5")
    print(f"Monthly Profit: ₹{int(example['monthly_profit'])}")
    print(f"Is Profitable: {'YES ✅' if example['is_profitable'] == 1 else 'NO ❌'}")
    
    # Save to CSV
    print("\n" + "="*60)
    print("💾 SAVING DATA")
    print("="*60)
    df.to_csv('products.csv', index=False)
    print("✅ Saved to 'products.csv'")
