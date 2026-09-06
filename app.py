"""
AmzDropship GCC Enterprise Suite | Amazon Profit Predictor & Global Capability Centre
An all-in-one suite for global Amazon sellers, dropshippers, and GCC enterprise hubs.
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
import os

from config import CATEGORY_MAPPING, MARKETPLACES
from gcc_engine import (
    convert_currency,
    calculate_cross_border_landed_cost,
    calculate_regional_tax,
    calculate_global_portfolio_kpis
)

# ============================================
# PAGE CONFIGURATION & BRANDING
# ============================================
st.set_page_config(
    page_title="AmzDropship GCC Enterprise | Global Capability Centre Suite",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Dark-Slate Theme Stylesheet
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        color: #f1f5f9;
    }
    
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p {
        color: #f8fafc !important;
        font-weight: 500 !important;
    }
    
    .custom-card {
        background: #1e293b;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .custom-card:hover {
        transform: translateY(-3px);
        border-color: #38bdf8;
        box-shadow: 0 20px 25px -5px rgba(56, 189, 248, 0.15);
    }
    
    .card-title {
        font-size: 0.85em;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    
    .card-value {
        font-size: 2em;
        font-weight: 700;
        color: #f8fafc;
        font-family: 'Outfit', sans-serif;
    }
    
    .card-delta {
        font-size: 0.88em;
        margin-top: 6px;
        font-weight: 500;
    }
    
    .text-green { color: #10b981; }
    .text-red { color: #f43f5e; }
    .text-blue { color: #0ea5e9; }
    .text-orange { color: #f97316; }
    .text-purple { color: #a855f7; }
    
    .alert-box {
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        border: 1px solid transparent;
        font-family: 'Inter', sans-serif;
    }
    
    .alert-success {
        background: rgba(16, 185, 129, 0.1);
        border-color: #10b981;
        color: #a7f3d0;
    }
    
    .alert-warning {
        background: rgba(244, 63, 94, 0.1);
        border-color: #f43f5e;
        color: #fecdd3;
    }
    
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, rgba(51, 65, 85, 0.1) 0%, #334155 50%, rgba(51, 65, 85, 0.1) 100%);
        margin: 30px 0;
    }
    
    .section-title {
        font-size: 1.8em;
        font-weight: 700;
        margin-bottom: 20px;
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(to right, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .footer {
        text-align: center;
        padding: 30px;
        color: #64748b;
        font-size: 0.85em;
        border-top: 1px solid #1e293b;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# LOAD MODELS & PIPELINE
# ============================================
@st.cache_resource
def load_ml_pipeline():
    if not os.path.exists('products.csv'):
        try:
            import data_generator
            df = data_generator.generate_dataset(1000)
            df.to_csv('products.csv', index=False)
        except Exception as e:
            st.error(f"Error generating dataset: {e}")
            
    if not os.path.exists('sales_model.pkl') or not os.path.exists('classifier_model.pkl') or not os.path.exists('scaler.pkl'):
        try:
            import model_trainer
            model_trainer.train_models()
        except Exception as e:
            st.error(f"Error training ML models: {e}")

    try:
        sales_model = pickle.load(open('sales_model.pkl', 'rb'))
        classifier_model = pickle.load(open('classifier_model.pkl', 'rb'))
        scaler = pickle.load(open('scaler.pkl', 'rb'))
        return sales_model, classifier_model, scaler
    except Exception as e:
        st.error(f"Failed to load ML models: {e}")
        return None, None, None

sales_model, classifier_model, scaler = load_ml_pipeline()

@st.cache_data
def load_products_database():
    if os.path.exists('products.csv'):
        return pd.read_csv('products.csv')
    return pd.DataFrame()

products_df = load_products_database()

# ============================================
# SIDEBAR NAVIGATION
# ============================================
st.sidebar.markdown("""
    <div style="text-align: center; padding: 15px 0;">
        <h2 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 1.5em; background: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🌐 GCC ENTERPRISE</h2>
        <p style="color: #94a3b8; font-size: 0.82em; font-weight: 500;">Global Capability Centre Hub</p>
    </div>
""", unsafe_allow_html=True)

menu_choice = st.sidebar.radio(
    "Select Enterprise Tool",
    [
        "🌐 GCC Executive Control Tower",
        "📈 AI Profit Predictor (Multi-Region)",
        "🚢 Cross-Border Logistics & Tariffs",
        "🔍 Product Research (Black Box)",
        "🔑 Keyword Research (Magnet)",
        "📝 Listing Analyzer (Scribbles)",
        "🧮 FBA vs FBM Calculator"
    ],
    index=0
)

st.sidebar.markdown("""
    <div style="position: fixed; bottom: 15px; font-size: 0.78em; color: #64748b; font-weight: 500;">
        🌍 Global Hub: US, EU, UK, UAE, IN<br>
        Version 3.0 Enterprise GCC
    </div>
""", unsafe_allow_html=True)

# REGION ENCODING MAPPING FOR ML MODEL
REGION_MAPPING = {'IN': 0, 'US': 1, 'EU': 2, 'UK': 3, 'UAE': 4}

# ============================================
# TOOL 1: GCC EXECUTIVE CONTROL TOWER
# ============================================
if menu_choice == "🌐 GCC Executive Control Tower":
    st.markdown('<h1 class="section-title">🌐 GCC Executive Control Tower</h1>', unsafe_allow_html=True)
    st.markdown("Consolidated multi-region dashboard for enterprise executives monitoring global Amazon marketplace performance.")
    
    # Currency target selection
    target_currency = st.selectbox("Reporting Base Currency", ["USD ($)", "INR (₹)", "EUR (€)", "GBP (£)", "AED"], index=0)
    curr_code = target_currency.split()[0]
    
    kpis = calculate_global_portfolio_kpis(products_df, target_currency=curr_code)
    
    # Top KPI Cards
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Consolidated Revenue</div>
                <div class="card-value">{kpis['symbol']}{kpis['global_revenue']:,.0f}</div>
                <div class="card-delta text-blue">{kpis['total_products']} Active Listings</div>
            </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Consolidated Net Profit</div>
                <div class="card-value text-green">{kpis['symbol']}{kpis['global_profit']:,.0f}</div>
                <div class="card-delta text-green">EBITDA Positive</div>
            </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Global Portfolio Margin</div>
                <div class="card-value text-purple">{kpis['avg_margin_pct']}%</div>
                <div class="card-delta text-purple">Net Portfolio Return</div>
            </div>
        """, unsafe_allow_html=True)
        
    with c4:
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Top Revenue Region</div>
                <div class="card-value">{kpis['top_region'].split()[0]}</div>
                <div class="card-delta text-orange">{kpis['top_region']} Hub</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Charts: Regional breakdown & Category contribution
    col_g1, col_g2 = st.columns([3, 2])
    
    with col_g1:
        st.subheader("📊 Marketplace Profitability by Region")
        if not products_df.empty:
            reg_df = products_df.groupby('marketplace_region').agg({
                'monthly_profit': 'sum',
                'monthly_sales': 'sum'
            }).reset_index()
            
            reg_df['region_name'] = reg_df['marketplace_region'].map(lambda x: MARKETPLACES[x]['name'])
            
            fig = px.bar(
                reg_df,
                x='region_name',
                y='monthly_profit',
                color='region_name',
                labels={'monthly_profit': f'Monthly Profit ({kpis["symbol"]})', 'region_name': 'Marketplace'},
                title="Regional Contribution Breakdown"
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                margin=dict(t=40, b=40, l=10, r=10)
            )
            st.plotly_chart(fig, use_container_width=True)
            
    with col_g2:
        st.subheader("🍕 Category Portfolio Distribution")
        if not products_df.empty:
            cat_df = products_df.groupby('category')['monthly_sales'].sum().reset_index()
            fig2 = px.pie(
                cat_df,
                names='category',
                values='monthly_sales',
                hole=0.4,
                title="Global Sales Volume Share"
            )
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                margin=dict(t=40, b=40, l=10, r=10)
            )
            st.plotly_chart(fig2, use_container_width=True)

# ============================================
# TOOL 2: MULTI-REGION AI PROFIT PREDICTOR
# ============================================
elif menu_choice == "📈 AI Profit Predictor (Multi-Region)":
    st.markdown('<h1 class="section-title">📊 Multi-Region AI Profit Predictor</h1>', unsafe_allow_html=True)
    st.markdown("Predict sales volume and winner probability across global Amazon marketplaces using Random Forest ML models.")
    
    if sales_model is None or classifier_model is None:
        st.error("⚠️ Machine Learning models not detected. Please train models first.")
    else:
        col_r, col_c = st.columns([1, 2])
        with col_r:
            selected_region_code = st.selectbox(
                "Select Marketplace Region",
                options=list(MARKETPLACES.keys()),
                format_func=lambda x: f"{MARKETPLACES[x]['country']} - {MARKETPLACES[x]['name']} ({MARKETPLACES[x]['currency']})"
            )
        
        market = MARKETPLACES[selected_region_code]
        sym = market['symbol']
        curr = market['currency']
        
        st.markdown(f"**Selected Marketplace:** {market['name']} | Base Currency: **{curr} ({sym})** | Tax Structure: **{market['tax_name']} ({int(market['default_tax_rate']*100)}%)**")
        
        col1, col2, col3 = st.columns(3)
        
        default_price = 2500.0 if curr == 'INR' else (35.0 if curr in ['USD', 'EUR', 'GBP'] else 120.0)
        default_cost = 800.0 if curr == 'INR' else (11.0 if curr in ['USD', 'EUR', 'GBP'] else 38.0)
        
        with col1:
            category = st.selectbox("Product Category", list(CATEGORY_MAPPING.keys()))
            selling_price = st.number_input(f"Retail Selling Price ({sym})", min_value=1.0, max_value=500000.0, value=default_price, step=5.0)
            cost_price = st.number_input(f"Supplier Cost Price ({sym})", min_value=0.5, max_value=400000.0, value=default_cost, step=2.0)
            
        with col2:
            rating = st.slider("Expected Customer Rating ⭐", min_value=1.0, max_value=5.0, value=4.3, step=0.1)
            num_reviews = st.number_input("Estimated Total Reviews", min_value=5, max_value=50000, value=350, step=10)
            competition = st.slider("Competition Intensity", min_value=1, max_value=5, value=3)
            
        with col3:
            listing_score = st.slider("Listing Quality Score (1-10)", min_value=1, max_value=10, value=7)
            ads_spend_pct = st.slider("Target ACOS / Ads Spend %", min_value=0, max_value=50, value=12) / 100.0
            fulfillment_type = st.radio("Fulfillment Mode", ["Amazon FBA", "Merchant FBM / 3PL"])
            
        # Fee & Tax Calculation
        ref_fee = selling_price * market['avg_referral_fee']
        closing_fee = market['closing_fee_tiers'][0][1]
        weight_fee = market['fba_base_weight_fee'] if fulfillment_type == "Amazon FBA" else 0.0
        
        amazon_fees = ref_fee + closing_fee + weight_fee
        tax_res = calculate_regional_tax(selling_price, cost_price, amazon_fees, selected_region_code)
        tax_cost = tax_res['total_tax_amount']
        ads_cost = selling_price * ads_spend_pct
        
        total_costs = cost_price + amazon_fees + tax_cost + ads_cost
        net_profit = selling_price - total_costs
        margin_pct = (net_profit / selling_price) if selling_price > 0 else 0
        
        # Predict via ML Pipeline
        cat_enc = CATEGORY_MAPPING[category]
        reg_enc = REGION_MAPPING[selected_region_code]
        
        input_df = pd.DataFrame([{
            'category_encoded': cat_enc,
            'region_encoded': reg_enc,
            'price': selling_price,
            'cost': cost_price,
            'rating': rating,
            'num_reviews': num_reviews,
            'competition': competition,
            'listing_score': listing_score
        }])
        
        scaled_input = scaler.transform(input_df)
        pred_sales = max(5, int(sales_model.predict(scaled_input)[0]))
        prob_success = classifier_model.predict_proba(scaled_input)[0][1]
        monthly_profit = net_profit * pred_sales
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.subheader("⚡ Prediction Results")
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
                <div class="custom-card">
                    <div class="card-title">Profit / Unit</div>
                    <div class="card-value">{sym}{net_profit:,.2f}</div>
                    <div class="card-delta text-green">{margin_pct*100:.1f}% margin</div>
                </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
                <div class="custom-card">
                    <div class="card-title">Est. Monthly Sales</div>
                    <div class="card-value">{pred_sales:,.0f} units</div>
                    <div class="card-delta text-blue">{sym}{selling_price * pred_sales:,.2f} Rev</div>
                </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
                <div class="custom-card">
                    <div class="card-title">Est. Monthly Profit</div>
                    <div class="card-value text-green">{sym}{monthly_profit:,.2f}</div>
                    <div class="card-delta text-green">{market['name']}</div>
                </div>
            """, unsafe_allow_html=True)
        with m4:
            color_cls = "text-green" if prob_success >= 0.60 else "text-red"
            st.markdown(f"""
                <div class="custom-card">
                    <div class="card-title">Winner Probability</div>
                    <div class="card-value {color_cls}">{prob_success*100:.1f}%</div>
                    <div class="card-delta {color_cls}">{'WINNER 🏆' if prob_success>=0.60 else 'RISKY ⚠️'}</div>
                </div>
            """, unsafe_allow_html=True)

# ============================================
# TOOL 3: CROSS-BORDER LOGISTICS & TARIFFS
# ============================================
elif menu_choice == "🚢 Cross-Border Logistics & Tariffs":
    st.markdown('<h1 class="section-title">🚢 Cross-Border Logistics & Landed Cost Engine</h1>', unsafe_allow_html=True)
    st.markdown("Calculate international shipping fees, sea/air freight, cargo insurance, and customs import tariffs.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Freight & Package Specs")
        sourcing_usd = st.number_input("Sourcing Cost per Unit (USD $)", min_value=0.1, max_value=5000.0, value=8.50, step=0.5)
        weight_kg = st.number_input("Package Weight (kg)", min_value=0.05, max_value=100.0, value=0.75, step=0.1)
        length_cm = st.number_input("Length (cm)", min_value=1.0, max_value=200.0, value=25.0)
        width_cm = st.number_input("Width (cm)", min_value=1.0, max_value=200.0, value=15.0)
        height_cm = st.number_input("Height (cm)", min_value=1.0, max_value=200.0, value=10.0)
        
        shipping_mode = st.radio("Logistics Freight Mode", ["Sea Freight (LCL/Container)", "Air Express Freight"])
        dest_region = st.selectbox("Destination Marketplace Region", list(MARKETPLACES.keys()), index=1)
        
    with col2:
        st.subheader("💰 Landed Cost & Tariff Output")
        mode_key = 'sea' if 'Sea' in shipping_mode else 'air'
        res = calculate_cross_border_landed_cost(
            sourcing_usd, weight_kg, length_cm, width_cm, height_cm,
            shipping_mode=mode_key, dest_region=dest_region
        )
        
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Total Landed Cost per Unit</div>
                <div class="card-value text-blue">${res['total_landed_usd']} USD</div>
                <div class="card-delta text-purple">Equivalent: {res['dest_currency_symbol']}{res['landed_cost_dest_currency']} ({MARKETPLACES[dest_region]['currency']})</div>
            </div>
        """, unsafe_allow_html=True)
        
        landed_breakdown = pd.DataFrame({
            'Component': ['Base Sourcing Cost', 'Freight Fee', 'Cargo Insurance (0.5%)', 'Customs Import Tariff (6%)', 'Total Landed Cost'],
            'Cost (USD $)': [f"${sourcing_usd:.2f}", f"${res['freight_cost_usd']:.2f}", f"${res['insurance_usd']:.2f}", f"${res['customs_duty_usd']:.2f}", f"${res['total_landed_usd']:.2f}"]
        })
        st.table(landed_breakdown)

# ============================================
# TOOL 4: PRODUCT RESEARCH (BLACK BOX)
# ============================================
elif menu_choice == "🔍 Product Research (Black Box)":
    st.markdown('<h1 class="section-title">🔍 Global Product Research (Black Box)</h1>', unsafe_allow_html=True)
    if products_df.empty:
        st.warning("No product database detected.")
    else:
        reg_filter = st.multiselect("Filter Marketplace Regions", options=list(MARKETPLACES.keys()), default=list(MARKETPLACES.keys()))
        filtered_df = products_df[products_df['marketplace_region'].isin(reg_filter)]
        st.dataframe(filtered_df[['product_name', 'category', 'marketplace_region', 'currency', 'price', 'cost', 'rating', 'monthly_sales', 'monthly_profit', 'is_profitable']], use_container_width=True)

# ============================================
# TOOL 5: KEYWORD RESEARCH (MAGNET)
# ============================================
elif menu_choice == "🔑 Keyword Research (Magnet)":
    st.markdown('<h1 class="section-title">🔑 Global Keyword Research (Magnet)</h1>', unsafe_allow_html=True)
    kw_input = st.text_input("Enter Seed Keyword", "earbuds")
    if kw_input:
        np.random.seed(len(kw_input))
        kw_list = [f"best {kw_input}", f"{kw_input} wireless", f"cheap {kw_input}", f"premium {kw_input}"]
        kw_data = [{'Keyword': k, 'Search Volume': int(np.random.exponential(10000)+1000), 'CPC Bid ($)': round(np.random.uniform(0.5, 4.5), 2)} for k in kw_list]
        st.dataframe(pd.DataFrame(kw_data), use_container_width=True)

# ============================================
# TOOL 6: LISTING ANALYZER (SCRIBBLES)
# ============================================
elif menu_choice == "📝 Listing Analyzer (Scribbles)":
    st.markdown('<h1 class="section-title">📝 Listing Optimization (Scribbles)</h1>', unsafe_allow_html=True)
    t_title = st.text_input("Product Title", "Premium Noise Cancelling Earbuds with Heavy Bass")
    score = 8 if len(t_title) >= 30 else 4
    st.metric("Listing Indexing Score", f"{score}/10")

# ============================================
# TOOL 7: FBA VS FBM CALCULATOR
# ============================================
elif menu_choice == "🧮 FBA vs FBM Calculator":
    st.markdown('<h1 class="section-title">🧮 FBA vs FBM vs 3PL Calculator</h1>', unsafe_allow_html=True)
    st.info("Side-by-side cost comparison for Amazon FBA vs Merchant FBM logistics.")

# ============================================
# FOOTER
# ============================================
st.markdown("""
    <div class="footer">
        <p>🌐 <b>AmzDropship Enterprise GCC Hub</b> | Global Capability Centre Suite</p>
        <p style="font-size: 0.85em; opacity: 0.7;">Multi-Market Analytics for US, Europe, UK, UAE, and India Seller Operations</p>
    </div>
""", unsafe_allow_html=True)
