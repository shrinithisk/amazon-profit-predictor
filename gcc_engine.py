"""
Global Capability Centre (GCC) Intelligence & Shared Services Engine
Calculates cross-border landed costs, multi-jurisdiction tax liabilities, currency conversions, and global portfolio rollups.
"""

from config import MARKETPLACES, FREIGHT_BENCHMARKS

def convert_currency(amount: float, from_curr: str, to_curr: str) -> float:
    """Converts money between supported currencies via base INR conversion rates."""
    if from_curr == to_curr:
        return amount
    
    # Find exchange rates to INR
    from_rate = 1.0
    to_rate = 1.0
    
    for m in MARKETPLACES.values():
        if m['currency'] == from_curr:
            from_rate = m['exchange_rate_to_inr']
        if m['currency'] == to_curr:
            to_rate = m['exchange_rate_to_inr']
            
    # Convert to INR first, then to target currency
    amount_in_inr = amount * from_rate
    return amount_in_inr / to_rate

def calculate_cross_border_landed_cost(
    sourcing_cost_usd: float,
    weight_kg: float,
    length_cm: float,
    width_cm: float,
    height_cm: float,
    shipping_mode: str = 'sea',
    dest_region: str = 'US'
) -> dict:
    """
    Calculates international logistics landed cost per unit including freight, insurance, and import tariffs.
    """
    dest_market = MARKETPLACES.get(dest_region, MARKETPLACES['US'])
    
    # Calculate volume CBM (Cubic Meters)
    cbm_per_unit = (length_cm * width_cm * height_cm) / 1000000.0
    
    if shipping_mode == 'air':
        freight_usd = weight_kg * FREIGHT_BENCHMARKS['air_freight_per_kg_usd']
    else: # sea freight
        freight_usd = max(0.5, cbm_per_unit * FREIGHT_BENCHMARKS['sea_freight_per_cbm_usd'])
        
    insurance_usd = (sourcing_cost_usd + freight_usd) * FREIGHT_BENCHMARKS['insurance_pct']
    customs_value_usd = sourcing_cost_usd + freight_usd + insurance_usd
    duty_usd = customs_value_usd * FREIGHT_BENCHMARKS['avg_customs_duty_pct']
    
    total_landed_usd = sourcing_cost_usd + freight_usd + insurance_usd + duty_usd
    
    # Convert to destination currency
    dest_curr = dest_market['currency']
    landed_dest_curr = convert_currency(total_landed_usd, 'USD', dest_curr)
    
    return {
        'sourcing_cost_usd': sourcing_cost_usd,
        'freight_cost_usd': round(freight_usd, 2),
        'insurance_usd': round(insurance_usd, 2),
        'customs_duty_usd': round(duty_usd, 2),
        'total_landed_usd': round(total_landed_usd, 2),
        'landed_cost_dest_currency': round(landed_dest_curr, 2),
        'dest_currency_symbol': dest_market['symbol'],
        'shipping_mode': shipping_mode.upper()
    }

def calculate_regional_tax(selling_price: float, cost_price: float, amazon_fees: float, region_code: str) -> dict:
    """
    Calculates multi-jurisdiction tax liability according to regional rules.
    - India: 18% GST (Output - Input Tax Credit) + 18% GST on Amazon fees
    - EU/UK: Included VAT rate calculation
    - US: Collected Sales Tax calculation
    - UAE: 5% VAT
    """
    market = MARKETPLACES.get(region_code, MARKETPLACES['IN'])
    tax_rate = market['default_tax_rate']
    tax_name = market['tax_name']
    
    if region_code == 'IN':
        # Indian GST offset model
        net_gst_gov = (selling_price - cost_price) * tax_rate
        amazon_fee_gst = amazon_fees * tax_rate
        total_tax = net_gst_gov + amazon_fee_gst
        tax_detail = f"Output GST - ITC + Fee GST ({int(tax_rate*100)}%)"
    elif region_code in ['EU', 'UK']:
        # VAT included in retail price
        net_vat = selling_price - (selling_price / (1.0 + tax_rate))
        total_tax = net_vat
        tax_detail = f"Destination {tax_name} ({int(tax_rate*100)}%)"
    elif region_code == 'US':
        # US Sales Tax (collected & passed through)
        total_tax = selling_price * tax_rate
        tax_detail = f"Est. State Nexus Sales Tax ({tax_rate*100:.1f}%)"
    else: # UAE
        total_tax = selling_price * tax_rate
        tax_detail = f"UAE VAT ({int(tax_rate*100)}%)"
        
    return {
        'tax_name': tax_name,
        'tax_rate_pct': round(tax_rate * 100, 1),
        'total_tax_amount': round(total_tax, 2),
        'tax_detail': tax_detail,
        'currency_symbol': market['symbol']
    }

def calculate_global_portfolio_kpis(df, target_currency='USD') -> dict:
    """Calculates consolidated executive KPIs across global marketplaces."""
    if df.empty:
        return {
            'total_products': 0, 'global_revenue': 0.0, 'global_profit': 0.0,
            'avg_margin_pct': 0.0, 'top_region': 'N/A', 'symbol': '$'
        }
        
    target_symbol = '$' if target_currency == 'USD' else '₹'
    
    # Calculate per-product revenue and profit converted to target currency
    revenues = []
    profits = []
    
    for _, row in df.iterrows():
        reg = row.get('marketplace_region', 'IN')
        market = MARKETPLACES.get(reg, MARKETPLACES['IN'])
        local_curr = market['currency']
        
        local_rev = row['price'] * row['monthly_sales']
        local_profit = row['monthly_profit']
        
        conv_rev = convert_currency(local_rev, local_curr, target_currency)
        conv_profit = convert_currency(local_profit, local_curr, target_currency)
        
        revenues.append(conv_rev)
        profits.append(conv_profit)
        
    tot_rev = sum(revenues)
    tot_prof = sum(profits)
    avg_margin = (tot_prof / tot_rev * 100.0) if tot_rev > 0 else 0.0
    
    # Identify top performing region
    region_profits = df.groupby('marketplace_region')['monthly_profit'].sum()
    top_reg_code = region_profits.idxmax() if not region_profits.empty else 'IN'
    top_reg_name = MARKETPLACES.get(top_reg_code, {}).get('name', 'India')
    
    return {
        'total_products': len(df),
        'global_revenue': round(tot_rev, 2),
        'global_profit': round(tot_prof, 2),
        'avg_margin_pct': round(avg_margin, 1),
        'top_region': top_reg_name,
        'symbol': target_symbol
    }
