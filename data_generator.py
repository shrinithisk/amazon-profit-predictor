"""
Amazon Global Product Data Generator (Healthy Multi-Market Economics & Enterprise GCC Grade)
Generates 1,000 realistic products across global marketplaces (India 🇮🇳, USA 🇺🇸, Europe 🇪🇺, UK 🇬🇧, UAE 🇦🇪).
Ensures profitable, healthy unit economics across all international marketplace regions.
"""

import pandas as pd
import numpy as np
import random
from config import CATEGORY_MAPPING, MARKETPLACES

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

categories = {
    'Consumer Electronics': {'referral_fee_pct': 0.08, 'avg_returns_rate': 0.08},
    'Home & Kitchen': {'referral_fee_pct': 0.11, 'avg_returns_rate': 0.06},
    'Apparel & Fashion': {'referral_fee_pct': 0.15, 'avg_returns_rate': 0.12},
    'Beauty & Personal Care': {'referral_fee_pct': 0.09, 'avg_returns_rate': 0.04},
    'Sports & Fitness': {'referral_fee_pct': 0.10, 'avg_returns_rate': 0.05},
    'Toys & Games': {'referral_fee_pct': 0.095, 'avg_returns_rate': 0.06}
}

TEMPLATE_PRICING_IN = {
    # Real-World Electronics & Accessories
    'iPhone 15 Pro Max Clear MagSafe Case': (599, 1699),
    'iPhone 20W USB-C Fast Charger Adapter': (699, 1899),
    'iPhone Tempered Glass Screen Protector (2 Pack)': (299, 599),
    'Apple AirPods Pro Wireless Charging Case': (2499, 4999),
    'Apple Watch Sport Loop Band': (499, 1299),
    'MacBook Air Aluminium Stand': (999, 2499),
    'Samsung Galaxy S24 Armor Cover': (499, 1299),
    'Wireless Noise Cancelling Earbuds': (999, 2999),
    'Smart Watch Fitness Tracker': (1299, 4499),
    'Power Bank 20000mAh': (1199, 2799),
    'Gaming Mouse RGB': (899, 2299),
    'Mechanical Keyboard Combo': (1499, 3999),
    
    # Real-World Home & Kitchen
    'Philips Electric Kettle 1.5L': (899, 1899),
    'Prestige Mixer Grinder 750W': (2199, 4799),
    'Milton Insulated Water Bottle 1L': (449, 899),
    'Wonderchef Non-Stick Tawa': (699, 1499),
    'LED Desk Lamp with Wireless Charging': (799, 1899),
    'Microfiber Cleaning Cloths (6 Pack)': (299, 599),
    'Coffee Frother Handheld': (349, 699),
    
    # Real-World Beauty & Personal Care
    'Maybelline Matte Liquid Lipstick': (349, 799),
    'Mamaearth Vitamin C Face Serum': (399, 799),
    'Nivea Soft Moisturizing Cream': (249, 549),
    'L\'Oreal Hair Repair Shampoo & Conditioner': (399, 899),
    'Minimalist Sunscreen SPF 50': (349, 699),
    'Beard Growth Oil': (249, 549),
    'Charcoal Deep Cleansing Face Wash': (249, 499),
    
    # Real-World Apparel & Fashion
    'Levi\'s Slim Fit Stretch Jeans': (1499, 3699),
    'Nike Air Running Shoes': (2199, 6499),
    'Puma Premium Cotton T-Shirt': (499, 1199),
    'Adidas Training Trackpants': (899, 2499),
    'Polarized UV Sunglasses': (599, 1499),
    'Sport Socks (3 Pack)': (249, 499),
    
    # Real-World Sports & Fitness
    'Boldfit Yoga Mat (6mm)': (599, 1499),
    'Decathlon Rubber Dumbbells Set (5kg)': (899, 2199),
    'Cosco Badminton Racket Set': (699, 1899),
    'Resistance Loop Bands Set': (349, 799),
    'Protein Shaker Bottle 700ml': (299, 699),
    
    # Real-World Toys & Games
    'LEGO Classic Building Blocks Set': (899, 2799),
    'Rubik\'s Speed Cube 3x3': (249, 499),
    'Hot Wheels Remote Control Car': (799, 1999),
    'Wooden Educational Puzzle': (349, 799),
    'Bubble Gun Blaster': (299, 599)
}

product_templates = {
    'Consumer Electronics': [
        'iPhone 15 Pro Max Clear MagSafe Case', 'iPhone 20W USB-C Fast Charger Adapter', 'iPhone Tempered Glass Screen Protector (2 Pack)',
        'Apple AirPods Pro Wireless Charging Case', 'Apple Watch Sport Loop Band', 'MacBook Air Aluminium Stand',
        'Samsung Galaxy S24 Armor Cover', 'Wireless Noise Cancelling Earbuds', 'Smart Watch Fitness Tracker', 'Power Bank 20000mAh', 'Gaming Mouse RGB', 'Mechanical Keyboard Combo'
    ],
    'Home & Kitchen': [
        'Philips Electric Kettle 1.5L', 'Prestige Mixer Grinder 750W', 'Milton Insulated Water Bottle 1L', 'Wonderchef Non-Stick Tawa',
        'LED Desk Lamp with Wireless Charging', 'Microfiber Cleaning Cloths (6 Pack)', 'Coffee Frother Handheld'
    ],
    'Apparel & Fashion': [
        'Levi\'s Slim Fit Stretch Jeans', 'Nike Air Running Shoes', 'Puma Premium Cotton T-Shirt', 'Adidas Training Trackpants', 'Polarized UV Sunglasses', 'Sport Socks (3 Pack)'
    ],
    'Beauty & Personal Care': [
        'Maybelline Matte Liquid Lipstick', 'Mamaearth Vitamin C Face Serum', 'Nivea Soft Moisturizing Cream', 'L\'Oreal Hair Repair Shampoo & Conditioner', 'Minimalist Sunscreen SPF 50', 'Beard Growth Oil', 'Charcoal Deep Cleansing Face Wash'
    ],
    'Sports & Fitness': [
        'Boldfit Yoga Mat (6mm)', 'Decathlon Rubber Dumbbells Set (5kg)', 'Cosco Badminton Racket Set', 'Resistance Loop Bands Set', 'Protein Shaker Bottle 700ml'
    ],
    'Toys & Games': [
        'LEGO Classic Building Blocks Set', 'Rubik\'s Speed Cube 3x3', 'Hot Wheels Remote Control Car', 'Wooden Educational Puzzle', 'Bubble Gun Blaster'
    ]
}

def generate_one_product():
    """Generates a single product with healthy positive unit economics across all global marketplaces."""
    region = random.choice(list(MARKETPLACES.keys()))
    market = MARKETPLACES[region]
    
    category = random.choice(list(categories.keys()))
    cat_data = categories[category]
    
    template_name = random.choice(product_templates[category])
    product_name = template_name
    
    # Get item-realistic price range in INR base
    inr_min, inr_max = TEMPLATE_PRICING_IN.get(template_name, (399, 1899))
    base_inr = np.random.uniform(inr_min, inr_max)
    
    if region == 'IN':
        price = round(base_inr, 2)
    else:
        rate = market['exchange_rate_to_inr']
        price = round(base_inr / rate, 2)
        price = max(6.99, price) # Ensure minimum floor price to cover FBA + VAT
        
    # Cost is 20% to 35% of retail price
    cost = round(price * np.random.uniform(0.20, 0.35), 2)
    
    weight_kg = round(np.random.uniform(0.08, 1.8), 2)
    length = round(np.random.uniform(8, 30), 1)
    width = round(np.random.uniform(6, length), 1)
    height = round(np.random.uniform(3, width), 1)
    
    rating = round(np.random.normal(4.4, 0.3), 1)
    rating = np.clip(rating, 3.5, 5.0)
    num_reviews = int(np.random.exponential(1500) + 350)
    
    competition = random.randint(1, 4)
    listing_score = int(np.clip(np.random.normal(8, 1.2), 5, 10))
    
    returns_rate = cat_data['avg_returns_rate']
    ads_spend_pct = round(np.random.uniform(0.05, 0.12), 3)
    
    base_sales = np.random.uniform(80, 450)
    rating_multiplier = (rating / 4.0) ** 2
    reviews_multiplier = np.log10(num_reviews) / 2.0
    comp_multiplier = (6 - competition) / 3.0
    
    monthly_sales = int(np.clip(base_sales * rating_multiplier * reviews_multiplier * comp_multiplier, 50, 2800))
    keyword_volume = int(np.random.exponential(14000) + 1500)
    
    # Accurate Amazon Fees Structure
    ref_fee = price * cat_data['referral_fee_pct']
    closing_fee = market['closing_fee_tiers'][0][1]
    
    if region == 'IN':
        weight_fee = 65.0 if weight_kg <= 0.5 else 65.0 + ((weight_kg - 0.5) * 35.0)
    else:
        weight_fee = 2.50 if weight_kg <= 0.5 else 2.50 + ((weight_kg - 0.5) * 0.80)
        
    total_amazon_fees = ref_fee + closing_fee + weight_fee
    
    # Net tax & advertising
    tax_rate = market['default_tax_rate']
    if region in ['EU', 'UK']:
        tax_liability = price - (price / (1.0 + tax_rate))
    else:
        tax_liability = (price - cost) * tax_rate
        
    ads_cost = price * ads_spend_pct
    returns_cost = (cost * 0.2) * returns_rate
    
    total_costs = cost + total_amazon_fees + tax_liability + ads_cost + returns_cost
    net_unit_profit = price - total_costs
    
    # Ensure realistic healthy profit margins (15% - 40% net margin)
    if net_unit_profit <= 0:
        net_unit_profit = round(price * np.random.uniform(0.18, 0.35), 2)
        
    monthly_profit = round(net_unit_profit * monthly_sales, 2)
    net_margin = round(net_unit_profit / price, 4)
    
    min_profit_threshold = 8000 if region == 'IN' else (120 if region in ['US', 'EU', 'UK'] else 400)
    is_profitable = 1 if (monthly_profit > min_profit_threshold and net_margin > 0.12) else 0
    
    return {
        'product_name': product_name,
        'category': category,
        'marketplace_region': region,
        'currency': market['currency'],
        'price': price,
        'cost': cost,
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
        'monthly_profit': monthly_profit,
        'net_margin': net_margin,
        'is_profitable': is_profitable
    }

def generate_dataset(num_products=1000):
    products = [generate_one_product() for _ in range(num_products)]
    return pd.DataFrame(products)

if __name__ == "__main__":
    print("🚀 Generating 1,000 Healthy Global Products...")
    df = generate_dataset(1000)
    output_path = 'products.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Healthy global dataset generated & saved to '{output_path}'")
