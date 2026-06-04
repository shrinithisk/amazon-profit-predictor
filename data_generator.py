"""
Amazon Product Data Generator (For India - Helium 10 Grade)
Generates 1,000 realistic Amazon India products for dropshipping/FBA sellers.
Includes weight, dimensions, Category referral fees, FBA storage/fulfillment fees,
return rates, and marketing/advertising costs. All prices in Indian Rupees (₹).
"""

import pandas as pd
import numpy as np
import random
import os

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================
# Category Configuration with Referral Fees & Realistic Dimensions
# ============================================
categories = {
    'Consumer Electronics': {
        'referral_fee_pct': 0.08,  # 8% average
        'price_range': (800, 15000),
        'weight_range': (0.1, 3.0),  # kg
        'size_range': (10, 40),      # cm (L, W, H)
        'avg_returns_rate': 0.12,    # 12% returns (high for electronics)
    },
    'Home & Kitchen': {
        'referral_fee_pct': 0.11,  # 11% average
        'price_range': (400, 8000),
        'weight_range': (0.3, 5.0),
        'size_range': (15, 50),
        'avg_returns_rate': 0.08,
    },
    'Apparel & Fashion': {
        'referral_fee_pct': 0.15,  # 15% average
        'price_range': (300, 4000),
        'weight_range': (0.1, 0.8),
        'size_range': (10, 30),
        'avg_returns_rate': 0.18,    # Very high returns (sizing issues)
    },
    'Beauty & Personal Care': {
        'referral_fee_pct': 0.09,  # 9% average
        'price_range': (200, 3000),
        'weight_range': (0.05, 0.5),
        'size_range': (5, 20),
        'avg_returns_rate': 0.05,    # Low returns
    },
    'Sports & Fitness': {
        'referral_fee_pct': 0.10,  # 10% average
        'price_range': (500, 12000),
        'weight_range': (0.5, 10.0),
        'size_range': (20, 80),
        'avg_returns_rate': 0.07,
    },
    'Toys & Games': {
        'referral_fee_pct': 0.095,  # 9.5% average
        'price_range': (250, 4000),
        'weight_range': (0.2, 2.0),
        'size_range': (10, 40),
        'avg_returns_rate': 0.09,
    }
}

product_templates = {
    'Consumer Electronics': ['Wireless Earbuds', 'Smart Watch', 'Bluetooth Speaker', 'Fast Charger Adapter', 'Power Bank', 'HDMI Cable', 'Gaming Mouse', 'Keyboard Combo', 'USB Ring Light', 'Phone Tripod'],
    'Home & Kitchen': ['Mixer Grinder', 'Electric Kettle', 'Non-Stick Tawa', 'Water Bottle (1L)', 'Organizer Box', 'LED Desk Lamp', 'Curtain Rod Set', 'Microfiber Cloths', 'Coffee Frother', 'Spice Rack'],
    'Apparel & Fashion': ['Cotton T-Shirt', 'Slim Fit Jeans', 'Running Shoes', 'Formal Leather Belt', 'Polarized Sunglasses', 'Casual Blazer', 'Sport Socks (3 Pack)', 'Hoodie Sweatshirt', 'Sling Bag', 'Trackpants'],
    'Beauty & Personal Care': ['Face Serum (Vitamin C)', 'Moisturizing Cream', 'Charcoal Face Wash', 'Beard Oil', 'Matte Lipstick', 'Shampoo & Conditioner', 'Hair Dryer', 'Sunscreen SPF 50', 'Essential Oil', 'Manicure Kit'],
    'Sports & Fitness': ['Yoga Mat (6mm)', 'Dumbbells Set (5kg)', 'Resistance Bands', 'Protein Shaker Bottle', 'Badminton Racket Set', 'Skipping Rope', 'Cricket Bat', 'Hand Grip Strengthener', 'Gym Bag', 'Cycling Helmet'],
    'Toys & Games': ['Rubik\'s Cube 3x3', 'Building Blocks Set', 'Remote Control Car', 'Wooden Puzzle', 'Doctor Play Set', 'Board Game (Ludo/Chess)', 'Modeling Clay Set', 'Soft Toy (Teddy)', 'Bubble Gun', 'Art & Craft Kit']
}

def calculate_closing_fee(price):
    """Amazon India closing fee based on item price bands"""
    if price <= 250:
        return 12.0
    elif price <= 500:
        return 20.0
    elif price <= 1000:
        return 40.0
    else:
        return 65.0

def calculate_fba_weight_fee(weight_kg, length, width, height):
    """Calculates FBA weight handling fee based on physical or dimensional weight (whichever is higher)"""
    dim_weight = (length * width * height) / 5000.0
    billable_weight = max(weight_kg, dim_weight)
    
    # Amazon India FBA national rate model (simplified)
    # First 500g (0.5kg) = ₹65
    # Next 500g up to 1kg = +₹25
    # Every additional 1kg beyond 1kg = +₹35
    if billable_weight <= 0.5:
        return 65.0
    elif billable_weight <= 1.0:
        return 65.0 + 25.0
    else:
        additional_kg = np.ceil(billable_weight - 1.0)
        return 65.0 + 25.0 + (additional_kg * 35.0)

def generate_one_product():
    """Generates a single product with comprehensive Helium 10 style variables"""
    category = random.choice(list(categories.keys()))
    cat_data = categories[category]
    
    # Sourcing basic template name
    template_name = random.choice(product_templates[category])
    brand_prefix = random.choice(['Bold', 'Solimo', 'Vibe', 'Nexa', 'Eco', 'Fit', 'Pro', 'Aura'])
    product_name = f"{brand_prefix} {template_name}"
    
    # Price and Cost
    p_min, p_max = cat_data['price_range']
    price = round(np.random.uniform(p_min, p_max), 0)
    
    # Cost is usually 25% to 50% of price (representing healthy dropshipping margin or standard sourcing)
    cost_pct = np.random.uniform(0.25, 0.50)
    cost = round(price * cost_pct, 0)
    
    # Sizing variables
    w_min, w_max = cat_data['weight_range']
    weight_kg = round(np.random.uniform(w_min, w_max), 2)
    
    s_min, s_max = cat_data['size_range']
    length = round(np.random.uniform(s_min, s_max), 1)
    width = round(np.random.uniform(s_min * 0.7, length), 1)
    height = round(np.random.uniform(s_min * 0.3, width), 1)
    
    # Rating & Reviews
    # Higher sales volume products tend to have more reviews and higher ratings
    if random.random() < 0.75:
        rating = round(np.random.normal(4.3, 0.3), 1)
        num_reviews = int(np.random.exponential(800) + 150)
    else:
        rating = round(np.random.normal(3.2, 0.5), 1)
        num_reviews = int(np.random.exponential(150) + 10)
    rating = np.clip(rating, 1.0, 5.0)
    num_reviews = max(5, num_reviews)
    
    # Competition level (1-5) & Listing Quality Score (1-10)
    competition = random.randint(1, 5)
    listing_score = int(np.clip(np.random.normal(7, 1.5), 1, 10))
    
    # Returns Rate (influenced by category & rating)
    returns_rate = cat_data['avg_returns_rate']
    if rating < 3.5:
        returns_rate += np.random.uniform(0.05, 0.15)  # low ratings increase return rate
    returns_rate = round(np.clip(returns_rate, 0.02, 0.35), 3)
    
    # Marketing and Ads Spend (ACOS / Ads spend pct of sales price)
    ads_spend_pct = round(np.random.uniform(0.05, 0.18), 3)
    
    # Simulated sales: higher rating, higher reviews, lower price, lower competition increases sales
    base_sales = np.random.uniform(20, 200)
    rating_multiplier = (rating / 4.0) ** 2
    reviews_multiplier = np.log10(num_reviews) / 2.0
    comp_multiplier = (6 - competition) / 3.0
    price_multiplier = 1.0 + max(0, (5000 - price) / 10000.0)
    
    monthly_sales = int(np.clip(base_sales * rating_multiplier * reviews_multiplier * comp_multiplier * price_multiplier, 5, 1200))
    
    # Keyword search volume (Magnet style indicator)
    keyword_volume = int(np.random.exponential(8000) + 800)
    if monthly_sales > 300:
        keyword_volume += int(np.random.uniform(5000, 25000))
    
    # --- Fee Calculations ---
    referral_fee = price * cat_data['referral_fee_pct']
    closing_fee = calculate_closing_fee(price)
    fba_weight_fee = calculate_fba_weight_fee(weight_kg, length, width, height)
    fba_storage_fee = (length * width * height) / 1000000.0 * 25.0  # ₹25 per cubic decimeter/month
    
    # Total Amazon Fees
    amazon_fees = referral_fee + closing_fee + fba_weight_fee + fba_storage_fee
    
    # GST calculation:
    # 18% GST collected on Selling Price
    # 18% GST paid on Sourcing Cost (offset as Input Tax Credit - ITC)
    # 18% GST paid on Amazon Fees (cost to seller, cannot offset)
    net_gst_to_gov = (price - cost) * 0.18
    amazon_fees_gst = amazon_fees * 0.18
    total_tax_liability = net_gst_to_gov + amazon_fees_gst
    
    # Marketing & Return Cost (sourcing loss & shipping loss)
    ads_cost = price * ads_spend_pct
    # Returns cost calculation: Returned units lose FBA fees + 50% sourcing cost (unsellable) + return shipping
    returns_cost_per_returned_unit = (fba_weight_fee * 1.5) + (cost * 0.5)
    total_returns_monthly_cost = (monthly_sales * returns_rate) * returns_cost_per_returned_unit
    returns_cost_per_unit = total_returns_monthly_cost / monthly_sales
    
    # Total Cost per Unit (sourcing + amazon fees + amazon fee gst + ads + returns share)
    total_cost_per_unit = cost + amazon_fees + amazon_fees_gst + ads_cost + returns_cost_per_unit
    
    # Net Profit
    profit_per_unit = price - total_cost_per_unit - net_gst_to_gov
    monthly_profit = profit_per_unit * monthly_sales
    
    net_margin = (profit_per_unit / price)
    
    # Winner Criteria: Net Monthly Profit > ₹15,000 AND Net Margin > 15%
    is_profitable = 1 if (monthly_profit > 15000 and net_margin > 0.15) else 0
    
    return {
        'product_name': product_name,
        'category': category,
        'price': int(price),
        'cost': int(cost),
        'weight_kg': weight_kg,
        'length_cm': length,
        'width_cm': width,
        'height_cm': height,
        'referral_fee_pct': round(cat_data['referral_fee_pct'], 3),
        'rating': rating,
        'num_reviews': num_reviews,
        'competition': competition,
        'listing_score': listing_score,
        'returns_rate': returns_rate,
        'ads_spend_pct': ads_spend_pct,
        'keyword_volume': keyword_volume,
        'monthly_sales': monthly_sales,
        'monthly_profit': round(monthly_profit, 2),
        'net_margin': round(net_margin, 4),
        'is_profitable': is_profitable
    }

def generate_dataset(num_products=1000):
    products = []
    for i in range(num_products):
        products.append(generate_one_product())
    df = pd.DataFrame(products)
    return df

if __name__ == "__main__":
    print("🚀 Generating 1,000 premium Helium 10-style Amazon India products...")
    df = generate_dataset(1000)
    
    # Ensure folder path exists
    output_path = 'products.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✅ Generated dataset and saved to '{output_path}'")
    print(f"Total Rows: {len(df)}")
    print(f"Profitable Products: {df['is_profitable'].sum()} ({df['is_profitable'].mean()*100:.1f}%)")
    print(f"Avg Price: ₹{df['price'].mean():.2f}")
    print(f"Avg Margin: {df['net_margin'].mean()*100:.2f}%")
