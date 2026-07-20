"""
Amazon Profit Predictor Pro (Helium 10 Alternative for India)
An all-in-one suite of tools for Amazon India dropshipping & FBA sellers.
Includes:
1. 📈 AI Profit Predictor & Dashboard
2. 🔍 Product Research (Black Box)
3. 🔑 Keyword Research (Magnet)
4. 📝 Listing Analyzer (Scribbles)
5. 🧮 FBA vs FBM vs Dropshipping Cost Calculator
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
import os

# ============================================
# PAGE CONFIGURATION & BRANDING
# ============================================
st.set_page_config(
    page_title="AmzDropship Pro | Amazon Profit Predictor Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Dark-Slate Theme Stylesheet
st.markdown("""
    <style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        color: #f1f5f9;
    }
    
    /* Background Styling */
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    
    /* Ensure Sidebar Titles & Option Labels are Fully Visible (White/Light Gray) */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div[role="radiogroup"] label p {
        color: #f8fafc !important;
        font-weight: 500 !important;
    }
    
    /* Ensure the Select Tool label has good contrast */
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
    
    /* Metric Card Custom Style */
    .custom-card {
        background: #1e293b;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .custom-card:hover {
        transform: translateY(-4px);
        border-color: #0ea5e9;
        box-shadow: 0 20px 25px -5px rgba(14, 165, 233, 0.15);
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
        font-size: 0.9em;
        margin-top: 6px;
        font-weight: 500;
    }
    
    .text-green { color: #10b981; }
    .text-red { color: #f43f5e; }
    .text-blue { color: #0ea5e9; }
    .text-orange { color: #f97316; }
    
    /* Alert Boxes */
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
    
    /* Styled buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1em !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 6px -1px rgba(2, 132, 199, 0.2) !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 15px -3px rgba(2, 132, 199, 0.4) !important;
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
    }
    
    /* Custom divider styling */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, rgba(51, 65, 85, 0.1) 0%, #334155 50%, rgba(51, 65, 85, 0.1) 100%);
        margin: 40px 0;
    }
    
    /* Section Title Custom styling */
    .section-title {
        font-size: 1.8em;
        font-weight: 700;
        margin-bottom: 24px;
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(to right, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Scrollbar customization */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0f172a;
    }
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #0ea5e9;
    }
    
    /* Footers */
    .footer {
        text-align: center;
        padding: 40px;
        color: #64748b;
        font-size: 0.85em;
        border-top: 1px solid #1e293b;
        margin-top: 60px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# LOAD MODELS & SCALER
# ============================================
@st.cache_resource
def load_ml_pipeline():
    # Generate products database if missing
    if not os.path.exists('products.csv'):
        try:
            import data_generator
            df = data_generator.generate_dataset(1000)
            df.to_csv('products.csv', index=False)
        except Exception as e:
            st.error(f"Error generating dataset on the fly: {e}")
            
    # Train models if missing
    if not os.path.exists('sales_model.pkl') or not os.path.exists('classifier_model.pkl') or not os.path.exists('scaler.pkl'):
        try:
            import model_trainer
            model_trainer.train_models()
        except Exception as e:
            st.error(f"Error training models on the fly: {e}")

    try:
        Review security policy for this programming language
        classifier_model = pickle.load(open('classifier_model.pkl', 'rb'))
        scaler = pickle.load(open('scaler.pkl', 'rb'))
        return sales_model, classifier_model, scaler
    except FileNotFoundError:
        return None, None, None

sales_model, classifier_model, scaler = load_ml_pipeline()

CATEGORY_MAPPING = {
    'Consumer Electronics': 0,
    'Home & Kitchen': 1,
    'Apparel & Fashion': 2,
    'Beauty & Personal Care': 3,
    'Sports & Fitness': 4,
    'Toys & Games': 5
}

# ============================================
# HELPER DATA GENERATION / RETRIEVAL
# ============================================
@st.cache_data
def load_products_database():
    if os.path.exists('products.csv'):
        return pd.read_csv('products.csv')
    return pd.DataFrame() # Return empty if generator hasn't run

products_df = load_products_database()

# ============================================
# SIDEBAR NAVIGATION
# ============================================
st.sidebar.markdown("""
    <div style="text-align: center; padding: 15px 0;">
        <h2 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 1.6em; background: linear-gradient(135deg, #38bdf8 0%, #0369a1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">⚡ SELLER PRO</h2>
        <p style="color: #94a3b8; font-size: 0.85em; font-weight: 500;">AmzDropship Pro Suite</p>
    </div>
""", unsafe_allow_html=True)

menu_choice = st.sidebar.radio(
    "Select Tool",
    [
        "📈 AI Profit Predictor",
        "🔍 Product Research (Black Box)",
        "🔑 Keyword Research (Magnet)",
        "📝 Listing Analyzer (Scribbles)",
        "🧮 FBA vs FBM Calculator"
    ],
    index=0
)

st.sidebar.markdown("""
    <div style="position: fixed; bottom: 20px; font-size: 0.8em; color: #64748b; font-weight: 500;">
        🇮🇳 Tailored for Amazon.in (₹)<br>
        Version 2.0 (Premium)
    </div>
""", unsafe_allow_html=True)

# ============================================
# TOOL 1: AI PROFIT PREDICTOR & DASHBOARD
# ============================================
if menu_choice == "📈 AI Profit Predictor":
    st.markdown('<h1 class="section-title">📊 AI Profit Predictor & Sourcing Dashboard</h1>', unsafe_allow_html=True)
    
    if sales_model is None or classifier_model is None:
        st.error("⚠️ Machine Learning models not detected. Please run model_trainer.py to train and export the models.")
    else:
        st.markdown("Predict the success rating of new items using Random Forest models trained on simulated Amazon products.")
        
        # User input panels
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            category = st.selectbox("Product Category", list(CATEGORY_MAPPING.keys()))
            selling_price = st.number_input("Selling Price on Amazon (₹)", min_value=100, max_value=100000, value=2500, step=50)
            cost_price = st.number_input("Supplier Sourcing Cost (₹)", min_value=20, max_value=90000, value=750, step=50)
        
        with col2:
            rating = st.slider("Expected Customer Rating", min_value=1.0, max_value=5.0, value=4.3, step=0.1)
            num_reviews = st.number_input("Estimated Total Reviews", min_value=5, max_value=20000, value=350, step=10)
            competition = st.slider("Competition Intensity", min_value=1, max_value=5, value=3, help="1 = Very Low, 5 = Saturation")
            
        with col3:
            listing_score = st.slider("Listing Quality Score (1-10)", min_value=1, max_value=10, value=7, help="Estimated optimization score of the product page")
            ads_spend_pct = st.slider("Target Ads Spend (ACOS % of price)", min_value=0, max_value=50, value=10) / 100.0
            fulfillment_type = st.radio("Fulfillment Model", ["Amazon FBA", "Merchant FBM / Dropship"])
            
        # Perform fee calculations on input
        # Standard constants mimicking data generator
        referral_fee_pcts = {
            'Consumer Electronics': 0.08, 'Home & Kitchen': 0.11, 'Apparel & Fashion': 0.15,
            'Beauty & Personal Care': 0.09, 'Sports & Fitness': 0.10, 'Toys & Games': 0.095
        }
        ref_fee_pct = referral_fee_pcts[category]
        referral_fee = selling_price * ref_fee_pct
        
        # Closing fee
        if selling_price <= 250: closing_fee = 12.0
        elif selling_price <= 500: closing_fee = 20.0
        elif selling_price <= 1000: closing_fee = 40.0
        else: closing_fee = 65.0
            
        if fulfillment_type == "Amazon FBA":
            # Assume 1kg package standard size for calculation
            weight_fee = 90.0 # Standard local/national FBA weight fee
            storage_fee = 15.0 # Basic monthly volume fee
            ship_and_pack = 0.0
        else:
            weight_fee = 0.0
            storage_fee = 0.0
            ship_and_pack = 70.0 # Estimated self shipping & packaging
            
        amazon_fees = referral_fee + closing_fee + weight_fee + storage_fee
        amazon_fees_gst = amazon_fees * 0.18
        net_gst = (selling_price - cost_price) * 0.18
        ads_cost = selling_price * ads_spend_pct
        
        # Dropship returns allowance
        returns_rate = 0.12 if category == 'Apparel & Fashion' else 0.07
        returns_cost = (returns_rate * (cost_price * 0.5 + (weight_fee or ship_and_pack))) 
        
        total_costs = cost_price + amazon_fees + amazon_fees_gst + net_gst + ads_cost + ship_and_pack + returns_cost
        net_unit_profit = selling_price - total_costs
        margin_pct = (net_unit_profit / selling_price)
        
        # Run prediction
        encoded_cat = CATEGORY_MAPPING[category]
        features_df = pd.DataFrame([{
            'category_encoded': encoded_cat,
            'price': selling_price,
            'cost': cost_price,
            'rating': rating,
            'num_reviews': num_reviews,
            'competition': competition,
            'listing_score': listing_score
        }])
        
        scaled_features = scaler.transform(features_df)
        predicted_sales = max(5, int(sales_model.predict(scaled_features)[0]))
        prob_success = classifier_model.predict_proba(scaled_features)[0][1] # Probability of is_profitable
        
        est_monthly_profit = net_unit_profit * predicted_sales
        
        # Action button
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Metrics Display
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<h3 style="font-family: \'Outfit\'; margin-bottom: 20px;">⚡ Analysis Results</h3>', unsafe_allow_html=True)
        
        c_m1, c_m2, c_m3, c_m4 = st.columns(4)
        
        with c_m1:
            delta_color = "text-green" if net_unit_profit > 0 else "text-red"
            st.markdown(f"""
                <div class="custom-card">
                    <div class="card-title">Profit / Unit</div>
                    <div class="card-value">₹{net_unit_profit:,.0f}</div>
                    <div class="card-delta {delta_color}">{margin_pct*100:.1f}% margin</div>
                </div>
            """, unsafe_allow_html=True)
            
        with c_m2:
            st.markdown(f"""
                <div class="custom-card">
                    <div class="card-title">AI Est. Monthly Sales</div>
                    <div class="card-value">{predicted_sales:,.0f} units</div>
                    <div class="card-delta text-blue">₹{selling_price * predicted_sales:,.0f} Revenue</div>
                </div>
            """, unsafe_allow_html=True)
            
        with c_m3:
            delta_color = "text-green" if est_monthly_profit > 15000 else ("text-orange" if est_monthly_profit > 0 else "text-red")
            st.markdown(f"""
                <div class="custom-card">
                    <div class="card-title">AI Est. Monthly Profit</div>
                    <div class="card-value">₹{est_monthly_profit:,.0f}</div>
                    <div class="card-delta {delta_color}">₹{est_monthly_profit*12:,.0f} / year</div>
                </div>
            """, unsafe_allow_html=True)
            
        with c_m4:
            class_color = "text-green" if prob_success >= 0.65 else ("text-orange" if prob_success >= 0.40 else "text-red")
            success_lbl = "WINNER 🏆" if prob_success >= 0.65 else ("BORDERLINE ⚠️" if prob_success >= 0.40 else "RISKY ❌")
            st.markdown(f"""
                <div class="custom-card">
                    <div class="card-title">AI Winner Probability</div>
                    <div class="card-value {class_color}">{prob_success*100:.1f}%</div>
                    <div class="card-delta {class_color}">{success_lbl}</div>
                </div>
            """, unsafe_allow_html=True)
        # Success indicator card
        cost_pct = cost_price / selling_price
        if prob_success >= 0.65:
            st.markdown(f"""
                <div class="alert-box alert-success">
                    <h4 style="margin: 0; color: #10b981; font-weight:700;">✅ Highly Recommended Product</h4>
                    <p style="margin: 8px 0 0 0; opacity: 0.95; font-size: 0.95em;">
                        Our Random Forest classifier predicts a <b>{prob_success*100:.1f}%</b> probability that this product will cross the ₹15,000 net monthly profit bar with a net margin >15%. 
                        Sourcing prices, competitive levels, and simulated listings indicate healthy demand metrics. Go ahead and launch this batch!
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="alert-box alert-warning">
                    <h4 style="margin: 0; color: #f43f5e; font-weight:700;">⚠️ Margins or Sales Volatility Detected</h4>
                    <p style="margin: 8px 0 0 0; opacity: 0.95; font-size: 0.95em;">
                        The model evaluates this product's winner potential at only <b>{prob_success*100:.1f}%</b>. 
                        Common causes include high sourcing costs (over {cost_pct*100:.0f}% of price), heavy competition, or excessive return risk in {category}. 
                        Review supplier negotiations or adjust the retail pricing structure.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
        # Graphical breakdowns
        gcol1, gcol2 = st.columns([1, 1])
        
        with gcol1:
            # Sourcing breakdown chart
            cost_labels = ['Sourcing Cost', 'Amazon Fees', 'Tax GST', 'Ads Spend', 'Return Risk Loss', 'Net Profit']
            cost_values = [cost_price, amazon_fees, amazon_fees_gst + net_gst, ads_cost, returns_cost, max(0, net_unit_profit)]
            
            fig = go.Figure(data=[go.Pie(
                labels=cost_labels,
                values=cost_values,
                hole=.4,
                marker=dict(colors=['#475569', '#3b82f6', '#ef4444', '#f59e0b', '#8b5cf6', '#10b981']),
                textinfo='percent+label'
            )])
            
            fig.update_layout(
                title=dict(text="Cost & Profit Breakdown (Per Unit)", font=dict(color="#f1f5f9", size=16)),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                legend=dict(orientation="h", y=-0.1),
                margin=dict(t=50, b=50, l=10, r=10)
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with gcol2:
            # Sensitivity Analysis Line Chart
            prices_range = np.linspace(selling_price * 0.7, selling_price * 1.4, 20)
            margins_range = []
            
            for p in prices_range:
                # Recalculate margins
                cur_ref = p * ref_fee_pct
                if p <= 250: cur_cls = 12.0
                elif p <= 500: cur_cls = 20.0
                elif p <= 1000: cur_cls = 40.0
                else: cur_cls = 65.0
                
                cur_amz = cur_ref + cur_cls + weight_fee + storage_fee
                cur_amz_gst = cur_amz * 0.18
                cur_net_gst = (p - cost_price) * 0.18
                cur_ads = p * ads_spend_pct
                cur_tot_cost = cost_price + cur_amz + cur_amz_gst + cur_net_gst + cur_ads + ship_and_pack + returns_cost
                
                margins_range.append(((p - cur_tot_cost) / p) * 100.0)
                
            fig2 = px.line(
                x=prices_range,
                y=margins_range,
                labels={'x': 'Selling Price (₹)', 'y': 'Net Profit Margin (%)'},
                title="Pricing Sensitivity Analysis"
            )
            fig2.update_traces(line_color="#0ea5e9", line_width=3)
            fig2.add_vline(x=selling_price, line_dash="dash", line_color="#ef4444", annotation_text="Current Price")
            fig2.add_hline(y=15.0, line_dash="dash", line_color="#10b981", annotation_text="Target Margin (15%)")
            
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                xaxis=dict(showgrid=True, gridcolor='#1e293b'),
                yaxis=dict(showgrid=True, gridcolor='#1e293b'),
                margin=dict(t=50, b=50, l=10, r=10)
            )
            st.plotly_chart(fig2, use_container_width=True)

# ============================================
# TOOL 2: PRODUCT RESEARCH (BLACK BOX)
# ============================================
elif menu_choice == "🔍 Product Research (Black Box)":
    st.markdown('<h1 class="section-title">🔍 Product Research (AmzDropship Black Box)</h1>', unsafe_allow_html=True)
    st.markdown("Filter and search through the 1,000 product database to identify high-margin niche opportunities.")
    
    if products_df.empty:
        st.warning("⚠️ No products database found. Please run the `data_generator.py` script first.")
    else:
        # Filtering parameters in columns
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        
        with f_col1:
            sel_categories = st.multiselect("Category Select", options=list(products_df['category'].unique()), default=list(products_df['category'].unique()))
        with f_col2:
            min_price, max_price = st.slider("Price Range (₹)", min_value=100, max_value=15000, value=(500, 7500))
        with f_col3:
            min_sales = st.number_input("Min Monthly Sales (Units)", min_value=0, max_value=1500, value=50)
        with f_col4:
            max_comp = st.slider("Max Competition Level (1-5)", min_value=1, max_value=5, value=4)
            
        # Apply filters
        filtered_df = products_df[
            (products_df['category'].isin(sel_categories)) &
            (products_df['price'] >= min_price) &
            (products_df['price'] <= max_price) &
            (products_df['monthly_sales'] >= min_sales) &
            (products_df['competition'] <= max_comp)
        ]
        
        # Summary row
        s_c1, s_c2, s_c3, s_c4 = st.columns(4)
        with s_c1:
            st.metric("Products Found", f"{len(filtered_df)}")
        with s_c2:
            avg_p = filtered_df['price'].mean() if not filtered_df.empty else 0
            st.metric("Avg Selling Price", f"₹{avg_p:,.0f}")
        with s_c3:
            avg_m = filtered_df['net_margin'].mean() * 100 if not filtered_df.empty else 0
            st.metric("Avg Net Margin %", f"{avg_m:.1f}%")
        with s_c4:
            total_est_vol = (filtered_df['monthly_sales'] * filtered_df['price']).sum() if not filtered_df.empty else 0
            st.metric("Total Monthly Value", f"₹{total_est_vol:,.0f}")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display formatted table
        if filtered_df.empty:
            st.warning("No products match the selected criteria.")
        else:
            display_df = filtered_df.copy()
            # Clean columns for human reading
            display_df = display_df.rename(columns={
                'product_name': 'Product Title',
                'category': 'Category',
                'price': 'Price (₹)',
                'cost': 'Cost (₹)',
                'rating': 'Rating ⭐',
                'num_reviews': 'Reviews',
                'competition': 'Competition',
                'net_margin': 'Margin %',
                'monthly_sales': 'Est. Sales',
                'monthly_profit': 'Est. Profit (₹)'
            })
            
            # Format margin
            display_df['Margin %'] = (display_df['Margin %'] * 100).round(1).astype(str) + '%'
            
            cols_to_show = ['Product Title', 'Category', 'Price (₹)', 'Cost (₹)', 'Rating ⭐', 'Reviews', 'Competition', 'Est. Sales', 'Margin %', 'Est. Profit (₹)']
            
            st.dataframe(
                display_df[cols_to_show].sort_values(by="Est. Profit (₹)", ascending=False),
                use_container_width=True,
                height=450
            )

# ============================================
# TOOL 3: KEYWORD RESEARCH (MAGNET)
# ============================================
elif menu_choice == "🔑 Keyword Research (Magnet)":
    st.markdown('<h1 class="section-title">🔑 Keyword Research (Magnet / Cerebro)</h1>', unsafe_allow_html=True)
    st.markdown("Search for customer search term metrics, estimated volumes, CPC values, and competitive keyword ratios.")
    
    keyword_input = st.text_input("Enter Seed Keyword (e.g. 'mixer grinder', 'earbuds', 'yoga mat')", "earbuds")
    
    # Generate seed-based keyword data on the fly
    if keyword_input:
        np.random.seed(len(keyword_input)) # unique keyword metrics based on seed length
        
        keywords = [
            f"best {keyword_input}", f"{keyword_input} wireless", f"{keyword_input} under 1000",
            f"boat {keyword_input}", f"premium {keyword_input}", f"{keyword_input} online",
            f"mini {keyword_input}", f"{keyword_input} for home", f"waterproof {keyword_input}",
            f"{keyword_input} cheap", f"noise cancelling {keyword_input}", f"original {keyword_input}"
        ]
        
        keywords_data = []
        for kw in keywords:
            search_vol = int(np.random.exponential(12000) + 1200)
            trend_pct = round(np.random.uniform(-0.15, 0.45) * 100, 1)
            cpc_bid = round(np.random.uniform(8.0, 75.0), 2)
            comp_products = int(np.random.uniform(50, 4500))
            magnet_score = int(search_vol / (comp_products + 1) * 10)
            
            keywords_data.append({
                'Keyword Search Term': kw,
                'Search Volume': search_vol,
                'Volume Trend': f"{trend_pct:+.1f}%",
                'Avg CPC Bid (₹)': cpc_bid,
                'Comp. Sellers': comp_products,
                'Magnet Opportunity Score': min(100, max(5, magnet_score))
            })
            
        kw_df = pd.DataFrame(keywords_data)
        
        # Display cards
        kc1, kc2, kc3 = st.columns(3)
        with kc1:
            top_kw = kw_df.loc[kw_df['Search Volume'].idxmax()]
            st.metric("Highest Search Term", top_kw['Keyword Search Term'], f"{top_kw['Search Volume']} Vol")
        with kc2:
            avg_cpc = kw_df['Avg CPC Bid (₹)'].mean()
            st.metric("Avg Bid CPC (₹)", f"₹{avg_cpc:.2f}")
        with kc3:
            best_opp = kw_df.loc[kw_df['Magnet Opportunity Score'].idxmax()]
            st.metric("Top Opportunity Score", f"{best_opp['Magnet Opportunity Score']}/100", best_opp['Keyword Search Term'])
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Layout of Keyword Table & Volume Chart
        klcol, krcol = st.columns([3, 2])
        
        with klcol:
            st.subheader("🔑 Related Keyword Analysis")
            st.dataframe(kw_df.sort_values(by="Search Volume", ascending=False), use_container_width=True)
            
        with krcol:
            st.subheader("📊 Search Volume Metrics")
            fig = px.bar(
                kw_df.sort_values(by="Search Volume", ascending=True),
                x="Search Volume",
                y="Keyword Search Term",
                orientation='h',
                color="Magnet Opportunity Score",
                color_continuous_scale=px.colors.sequential.Viridis
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                xaxis=dict(showgrid=True, gridcolor='#1e293b'),
                yaxis=dict(showgrid=False),
                margin=dict(t=10, b=10, l=10, r=10)
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# TOOL 4: LISTING ANALYZER (SCRIBBLES)
# ============================================
elif menu_choice == "📝 Listing Analyzer (Scribbles)":
    st.markdown('<h1 class="section-title">📝 Listing Optimization (Scribbles Engine)</h1>', unsafe_allow_html=True)
    st.markdown("Analyze your listing text for Amazon search engine indexing quality in real-time.")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("📝 Edit Copy")
        t_title = st.text_input("Product Title (Ideal: 150-200 Chars)", "Premium Noise Cancelling Wireless Earbuds with Heavy Bass & IPX7 Waterproofing")
        
        bullet1 = st.text_input("Bullet Point 1", "HIGH-FIDELITY AUDIO: Experience crisp acoustics and deep, dynamic bass response.")
        bullet2 = st.text_input("Bullet Point 2", "ACTIVE NOISE CANCELLING: Built-in smart ANC blocks external ambient distractions.")
        bullet3 = st.text_input("Bullet Point 3", "24-HOUR BATTERY LIFE: Enjoy 6 hours of continuous playtime plus 18 extra hours with the compact case.")
        bullet4 = st.text_input("Bullet Point 4", "")
        bullet5 = st.text_input("Bullet Point 5", "")
        
        desc = st.text_area("Product Description (Ideal: >500 Chars)", "Our Premium Wireless Earbuds are engineered with cutting-edge audio drivers to provide clear, rich, and high-fidelity sound. Designed specifically for active lifestyles, it features IPX7 waterproofing so you can push through sweaty workouts or run in the rain without worry. Easy touch-sensitive controls allow you to skip tracks, change volume, and answer calls on the fly. Compatible with iOS and Android devices via Bluetooth 5.2.")
        
    with col2:
        st.subheader("⚡ Optimization Score")
        
        # Real-time listing scoring calculations
        score = 0
        suggestions = []
        
        # 1. Title Length
        t_len = len(t_title)
        if 150 <= t_len <= 200:
            score += 3
        elif 100 <= t_len < 150:
            score += 2
            suggestions.append("⚠️ Title is slightly short. Add descriptive keywords (e.g. dimensions, color, compatibility).")
        else:
            score += 1
            suggestions.append("❌ Title is too short/long. Adjust to the 150-200 character bracket for optimal indexing.")
            
        # 2. Bullet Points Checklist
        bullets = [bullet1, bullet2, bullet3, bullet4, bullet5]
        active_bullets = [b for b in bullets if len(b) > 10]
        if len(active_bullets) >= 5:
            score += 3
        elif len(active_bullets) >= 3:
            score += 2
            suggestions.append("⚠️ Provide exactly 5 bullet points to maximize customer information space.")
        else:
            score += 1
            suggestions.append("❌ Very few bullet points found. Write detailed features to answer customer FAQs.")
            
        # 3. Description Length
        d_len = len(desc)
        if d_len >= 500:
            score += 2
        elif 200 <= d_len < 500:
            score += 1
            suggestions.append("⚠️ Expand product description to at least 500 characters to leverage keyword placements.")
        else:
            suggestions.append("❌ Description is too thin. Include warranty details, box contents, and use cases.")
            
        # 4. Keyword presence check
        keyword_bank = ["premium", "waterproof", "warranty", "heavy", "compatible", "bass", "durable"]
        found_kw = [k for k in keyword_bank if k in t_title.lower() or any(k in b.lower() for b in active_bullets) or k in desc.lower()]
        
        if len(found_kw) >= 5:
            score += 2
        elif len(found_kw) >= 3:
            score += 1
            suggestions.append("⚠️ Add more high-volume indexing words: e.g. 'warranty', 'durable', 'compatible'.")
        else:
            suggestions.append("❌ Sourcing keywords not detected. Optimize the copy for better SEO rankings.")
            
        # UI Gauge representation
        c_score_color = "#10b981" if score >= 8 else ("#f97316" if score >= 5 else "#f43f5e")
        st.markdown(f"""
            <div style="background:#1e293b; padding:35px; border-radius:12px; border:2px solid {c_score_color}; text-align:center;">
                <div style="font-size:1.1em; color:#94a3b8; font-weight:600; text-transform:uppercase;">Listing Score</div>
                <div style="font-size:4.5em; font-weight:800; color:{c_score_color}; font-family:'Outfit';">{score}/10</div>
                <div style="color:#f8fafc; font-weight:500; margin-top:10px;">
                    { 'Excellent Listing! 🚀' if score >= 8 else ('Needs Optimization ⚠️' if score >= 5 else 'Poor Indexing Structure ❌') }
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("💡 Recommendations")
        
        if not suggestions:
            st.success("Your listing meets all search optimization guidelines!")
        else:
            for sug in suggestions:
                st.markdown(f"- {sug}")

# ============================================
# TOOL 5: ADVANCED FEE CALCULATOR
# ============================================
elif menu_choice == "🧮 FBA vs FBM Calculator":
    st.markdown('<h1 class="section-title">🧮 Cost Comparison (FBA vs FBM vs Dropship)</h1>', unsafe_allow_html=True)
    st.markdown("Deep-dive side-by-side fee structures to choose the best logistics route.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📦 Weight & Dimensions")
        weight = st.number_input("Package Weight (kg)", min_value=0.05, max_value=40.0, value=0.6, step=0.1)
        length_c = st.number_input("Length (cm)", min_value=1.0, max_value=150.0, value=25.0, step=1.0)
        width_c = st.number_input("Width (cm)", min_value=1.0, max_value=150.0, value=15.0, step=1.0)
        height_c = st.number_input("Height (cm)", min_value=1.0, max_value=150.0, value=8.0, step=1.0)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("💰 Pricing Variables")
        calc_price = st.number_input("Selling Retail Price (₹)", min_value=100, max_value=100000, value=1500)
        calc_cost = st.number_input("Supplier Sourcing Price (₹)", min_value=20, max_value=90000, value=450)
        
    with col2:
        st.subheader("⚖️ Logistics Model Fee Breakdown")
        
        # Sizing Calculations
        dim_w = (length_c * width_c * height_c) / 5000.0
        bill_w = max(weight, dim_w)
        
        # Referral fee (10% standard estimate for calculations)
        ref_fee = calc_price * 0.10
        
        # Closing fee
        if calc_price <= 250: cls_fee = 12.0
        elif calc_price <= 500: cls_fee = 20.0
        elif calc_price <= 1000: cls_fee = 40.0
        else: cls_fee = 65.0
            
        # Weight Handling FBA Fee
        if bill_w <= 0.5: fba_w_fee = 65.0
        elif bill_w <= 1.0: fba_w_fee = 90.0
        else: fba_w_fee = 90.0 + (np.ceil(bill_w - 1.0) * 35.0)
            
        # FBA Storage
        fba_stor = (length_c * width_c * height_c) / 1000000.0 * 25.0
        
        # FBM Ship/Pack estimate
        fbm_ship_pack = 75.0
        # Dropshipping Sourcing Fee
        dropship_processing = 40.0
        dropship_ship = 90.0
        
        # side-by-side structures
        fba_total_fees = ref_fee + cls_fee + fba_w_fee + fba_stor
        fbm_total_fees = ref_fee + cls_fee + fbm_ship_pack
        ds_total_fees = ref_fee + cls_fee + dropship_processing + dropship_ship
        
        # GST liability
        fba_gst = (calc_price - calc_cost) * 0.18 + (fba_total_fees * 0.18)
        fbm_gst = (calc_price - calc_cost) * 0.18 + (fbm_total_fees * 0.18)
        ds_gst = (calc_price - calc_cost) * 0.18 + (ds_total_fees * 0.18)
        
        # Net unit calculations
        fba_profit = calc_price - calc_cost - fba_total_fees - fba_gst
        fbm_profit = calc_price - calc_cost - fbm_total_fees - fbm_gst
        ds_profit = calc_price - calc_cost - ds_total_fees - ds_gst
        
        # Results Dataframe
        data_comparison = {
            'Cost Components (₹)': [
                'Selling Price', 'Sourcing Cost', 'Referral Fee (10%)',
                'Closing Fee', 'Shipping & Weight Fee', 'FBA Storage Fee',
                'Dropship Processing', 'GST Taxes (18%)', 'Total Logistics Expense', 'Net Profit Per Unit', 'Margin %'
            ],
            'Amazon FBA': [
                f"₹{calc_price}", f"-₹{calc_cost}", f"-₹{ref_fee:.0f}",
                f"-₹{cls_fee:.0f}", f"-₹{fba_w_fee:.0f}", f"-₹{fba_stor:.1f}",
                '--', f"-₹{fba_gst:.1f}", f"₹{fba_total_fees+fba_gst:.1f}", f"₹{fba_profit:.1f}", f"{(fba_profit/calc_price)*100:.1f}%"
            ],
            'Merchant FBM': [
                f"₹{calc_price}", f"-₹{calc_cost}", f"-₹{ref_fee:.0f}",
                f"-₹{cls_fee:.0f}", f"-₹{fbm_ship_pack:.0f}", '--',
                '--', f"-₹{fbm_gst:.1f}", f"₹{fbm_total_fees+fbm_gst:.1f}", f"₹{fbm_profit:.1f}", f"{(fbm_profit/calc_price)*100:.1f}%"
            ],
            'Dropshipping': [
                f"₹{calc_price}", f"-₹{calc_cost}", f"-₹{ref_fee:.0f}",
                f"-₹{cls_fee:.0f}", f"-₹{dropship_ship:.0f}", '--',
                f"-₹{dropship_processing:.0f}", f"-₹{ds_gst:.1f}", f"₹{ds_total_fees+ds_gst:.1f}", f"₹{ds_profit:.1f}", f"{(ds_profit/calc_price)*100:.1f}%"
            ]
        }
        
        compare_df = pd.DataFrame(data_comparison)
        st.dataframe(compare_df, use_container_width=True)
        
        # Bar Chart Comparison
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📊 Profit Margin Comparison")
        
        fig = go.Figure(data=[
            go.Bar(name='Net Profit per Unit', x=['Amazon FBA', 'Merchant FBM', 'Dropshipping'], y=[max(0, fba_profit), max(0, fbm_profit), max(0, ds_profit)], marker_color=['#10b981', '#3b82f6', '#8b5cf6'])
        ])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#1e293b', title="Profit in ₹"),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""
    <div class="footer">
        <p>📊 <b>AmzDropship Pro Suite</b> | Engineered for Indian Dropshipping & FBA Entrepreneurs</p>
        <p style="font-size: 0.85em; opacity: 0.7;">⚠️ Disclaimer: Estimations are modeled via Random Forest Regressors / Classifiers trained on synthetic Amazon India parameters. Always cross-verify storage rates with Seller Central guidelines before shipping inventory.</p>
    </div>
""", unsafe_allow_html=True)
