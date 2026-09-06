"""
Global Capability Centre (GCC) Configuration & Standards Module
Centralized constants, marketplace fee structures, tax rules, and currency conversion baselines.
"""

# Category mapping to ensure consistent encoding across ML models and UI
CATEGORY_MAPPING = {
    'Consumer Electronics': 0,
    'Home & Kitchen': 1,
    'Apparel & Fashion': 2,
    'Beauty & Personal Care': 3,
    'Sports & Fitness': 4,
    'Toys & Games': 5
}

# Supported Global Amazon Marketplaces
MARKETPLACES = {
    'IN': {
        'name': 'Amazon India',
        'country': 'India 🇮🇳',
        'currency': 'INR',
        'symbol': '₹',
        'exchange_rate_to_inr': 1.0,
        'default_tax_rate': 0.18, # GST 18%
        'tax_name': 'GST',
        'avg_referral_fee': 0.10,
        'closing_fee_tiers': [(250, 12.0), (500, 20.0), (1000, 40.0), (float('inf'), 65.0)],
        'fba_base_weight_fee': 65.0, # INR for first 0.5kg
        'fba_add_weight_fee': 35.0   # INR per addl kg
    },
    'US': {
        'name': 'Amazon US',
        'country': 'United States 🇺🇸',
        'currency': 'USD',
        'symbol': '$',
        'exchange_rate_to_inr': 84.0,
        'default_tax_rate': 0.07, # Avg US Sales Tax 7%
        'tax_name': 'State Sales Tax',
        'avg_referral_fee': 0.15,
        'closing_fee_tiers': [(float('inf'), 1.80)], # USD
        'fba_base_weight_fee': 3.50, # USD for first 0.5kg
        'fba_add_weight_fee': 0.80   # USD per addl kg
    },
    'EU': {
        'name': 'Amazon Europe',
        'country': 'Germany / EU 🇪🇺',
        'currency': 'EUR',
        'symbol': '€',
        'exchange_rate_to_inr': 91.0,
        'default_tax_rate': 0.19, # German VAT 19%
        'tax_name': 'EU VAT',
        'avg_referral_fee': 0.15,
        'closing_fee_tiers': [(float('inf'), 1.50)], # EUR
        'fba_base_weight_fee': 3.20, # EUR for first 0.5kg
        'fba_add_weight_fee': 0.75   # EUR per addl kg
    },
    'UK': {
        'name': 'Amazon UK',
        'country': 'United Kingdom 🇬🇧',
        'currency': 'GBP',
        'symbol': '£',
        'exchange_rate_to_inr': 108.0,
        'default_tax_rate': 0.20, # UK VAT 20%
        'tax_name': 'UK VAT',
        'avg_referral_fee': 0.15,
        'closing_fee_tiers': [(float('inf'), 1.20)], # GBP
        'fba_base_weight_fee': 2.80, # GBP for first 0.5kg
        'fba_add_weight_fee': 0.65   # GBP per addl kg
    },
    'UAE': {
        'name': 'Amazon UAE',
        'country': 'United Arab Emirates 🇦🇪',
        'currency': 'AED',
        'symbol': 'AED ',
        'exchange_rate_to_inr': 22.8,
        'default_tax_rate': 0.05, # UAE VAT 5%
        'tax_name': 'UAE VAT',
        'avg_referral_fee': 0.10,
        'closing_fee_tiers': [(float('inf'), 5.0)], # AED
        'fba_base_weight_fee': 10.0, # AED for first 0.5kg
        'fba_add_weight_fee': 2.5   # AED per addl kg
    }
}

# Cross-border freight & logistics benchmarks
FREIGHT_BENCHMARKS = {
    'air_freight_per_kg_usd': 8.50,
    'sea_freight_per_cbm_usd': 180.0,
    'avg_customs_duty_pct': 0.06, # 6% standard import tariff
    'insurance_pct': 0.005 # 0.5% cargo insurance
}
