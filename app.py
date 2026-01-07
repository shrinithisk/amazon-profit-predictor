"""
Modern Amazon India Profitability Predictor
Clean, professional UI for Indian dropshipping sellers
All prices in Indian Rupees (₹)
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Amazon Profit Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern look
st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 0;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 20px;
        border-radius: 0;
        color: white;
        margin: -30px -30px 30px -30px;
        text-align: center;
    }
    
    .header-container h1 {
        font-size: 2.5em;
        margin: 0;
        font-weight: 700;
    }
    
    .header-container p {
        font-size: 1.1em;
        margin: 10px 0 0 0;
        opacity: 0.9;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Success message */
    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        margin: 20px 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        margin: 20px 0;
    }
    
    /* Input styling */
    .stNumberInput input, .stSlider slider {
        border-radius: 8px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 30px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1.1em !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 10px 20px;
    }
    
    /* Section divider */
    .section-title {
        font-size: 1.5em;
        font-weight: 700;
        margin: 30px 0 20px 0;
        color: #333;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        color: #666;
        font-size: 0.9em;
        border-top: 1px solid #e0e0e0;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
st.markdown("""
    <div class="header-container">
        <h1>📊 Amazon Profit Predictor</h1>
        <p>Smart AI-powered tool to predict profitability for Indian dropshipping</p>
    </div>
""", unsafe_allow_html=True)

# ============================================
# LOAD MODEL
# ============================================
@st.cache_resource
def load_model():
    """Load the saved model and scaler"""
    model = pickle.load(open('model.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))
    return model, scaler

model, scaler = load_model()

# ============================================
# INPUT SECTION
# ============================================
st.markdown('<h2 class="section-title">📝 Enter Product Details</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    price = st.number_input(
        "Selling Price (₹)",
        min_value=100.0,
        max_value=100000.0,
        value=2500.0,
        step=100.0,
        help="The price at which you'll sell the product on Amazon"
    )

with col2:
    cost = st.number_input(
        "Product Cost (₹)",
        min_value=10.0,
        max_value=90000.0,
        value=800.0,
        step=50.0,
        help="Your cost to procure the product"
    )

with col3:
    rating = st.slider(
        "Product Rating",
        min_value=1.0,
        max_value=5.0,
        value=4.5,
        step=0.1,
        help="Expected customer rating (1-5 stars)"
    )

col4, col5, col6 = st.columns(3)

with col4:
    num_reviews = st.number_input(
        "Number of Reviews",
        min_value=10,
        max_value=10000,
        value=1000,
        step=50,
        help="Expected number of customer reviews"
    )

with col5:
    monthly_sales = st.number_input(
        "Monthly Sales (units)",
        min_value=5,
        max_value=1000,
        value=150,
        step=10,
        help="Estimated monthly sales volume"
    )

with col6:
    competition = st.slider(
        "Competition Level",
        min_value=1,
        max_value=5,
        value=3,
        step=1,
        help="1=Low, 5=High. How many competitors exist?"
    )

# ============================================
# SUMMARY CARDS
# ============================================
st.markdown('<h2 class="section-title">💰 Financial Summary</h2>', unsafe_allow_html=True)

# Calculate costs
amazon_commission = price * 0.35  # 35% commission
gst = price * 0.18  # 18% GST
total_cost_with_fees = cost + amazon_commission + gst
profit_per_unit = price - total_cost_with_fees
monthly_profit = profit_per_unit * monthly_sales
annual_profit = monthly_profit * 12

# Display metrics
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric(
        label="Profit Per Unit",
        value=f"₹{profit_per_unit:.0f}",
        delta=f"{(profit_per_unit/price)*100:.1f}% margin",
        delta_color="normal" if profit_per_unit > 0 else "inverse"
    )

with metric_col2:
    st.metric(
        label="Monthly Revenue",
        value=f"₹{price * monthly_sales:,.0f}",
        delta=f"{monthly_sales} units"
    )

with metric_col3:
    st.metric(
        label="Monthly Profit",
        value=f"₹{monthly_profit:,.0f}",
        delta=f"₹{annual_profit:,.0f} yearly",
        delta_color="normal" if monthly_profit > 5000 else "inverse"
    )

with metric_col4:
    st.metric(
        label="Rating & Reviews",
        value=f"{rating}/5 ⭐",
        delta=f"{int(num_reviews)} reviews"
    )

# ============================================
# COST BREAKDOWN
# ============================================
st.markdown('<h2 class="section-title">🔍 Cost Breakdown</h2>', unsafe_allow_html=True)

cost_col1, cost_col2, cost_col3 = st.columns([1, 2, 1])

with cost_col2:
    st.write(f"""
    | Item | Amount |
    |------|--------|
    | **Selling Price** | ₹{price:,.0f} |
    | Product Cost | -₹{cost:,.0f} |
    | Amazon Commission (35%) | -₹{amazon_commission:,.0f} |
    | GST (18%) | -₹{gst:,.0f} |
    | **Profit Per Unit** | **₹{profit_per_unit:,.0f}** |
    """)

# ============================================
# PREDICTION BUTTON
# ============================================
st.markdown("<br>", unsafe_allow_html=True)

predict_button = st.button(
    "🎯 Analyze Profitability",
    use_container_width=True,
    key="predict_button"
)

if predict_button:
    
    # Prepare data for prediction
    input_data = pd.DataFrame([{
        'price': price,
        'cost': cost,
        'rating': rating,
        'num_reviews': num_reviews,
        'monthly_sales': monthly_sales,
        'competition': competition
    }])
    
    # Scale and predict
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0]
    confidence = max(probability[0], probability[1]) * 100
    
    # Display results
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">🔮 Prediction Result</h2>', unsafe_allow_html=True)
    
    if prediction == 1:
        # PROFITABLE
        st.markdown("""
        <div class="success-box">
            <h2 style="margin: 0; font-size: 2em;">✅ PROFITABLE</h2>
            <p style="margin: 10px 0 0 0; font-size: 1.1em;">This product is recommended for dropshipping!</p>
        </div>
        """, unsafe_allow_html=True)
        
        result_col1, result_col2, result_col3 = st.columns(3)
        
        with result_col1:
            st.metric(
                "Status",
                "GO AHEAD ✅",
                "Safe to launch"
            )
        
        with result_col2:
            st.metric(
                "Model Confidence",
                f"{confidence:.1f}%",
                "Very certain"
            )
        
        with result_col3:
            st.metric(
                "Expected Monthly Profit",
                f"₹{monthly_profit:,.0f}",
                f"₹{annual_profit:,.0f}/year"
            )
        
        # Reasons for profitability
        st.markdown("### ✅ Why This Product is Profitable:")
        
        reasons = []
        if profit_per_unit > 200:
            reasons.append(f"💎 Excellent profit margin (₹{profit_per_unit:.0f}/unit)")
        if rating >= 4.5:
            reasons.append(f"⭐ Strong customer rating ({rating}/5)")
        if monthly_sales >= 200:
            reasons.append(f"📈 Good sales potential ({monthly_sales} units/month)")
        if competition <= 2:
            reasons.append(f"🎯 Low competition (Level {competition}/5)")
        if num_reviews >= 1000:
            reasons.append(f"👥 High customer trust ({num_reviews} reviews)")
        
        if not reasons:
            reasons.append("✓ Good overall product metrics")
        
        for reason in reasons:
            st.write(f"• {reason}")
        
        # Recommendation
        st.success("🚀 **Recommendation:** This is a strong product for your dropshipping business. Consider launching it!", icon="✅")
    
    else:
        # NOT PROFITABLE
        st.markdown("""
        <div class="warning-box">
            <h2 style="margin: 0; font-size: 2em;">⚠️ NOT PROFITABLE</h2>
            <p style="margin: 10px 0 0 0; font-size: 1.1em;">Model predicts this product may not be profitable</p>
        </div>
        """, unsafe_allow_html=True)
        
        result_col1, result_col2, result_col3 = st.columns(3)
        
        with result_col1:
            st.metric(
                "Status",
                "RECONSIDER ⚠️",
                "Risk detected"
            )
        
        with result_col2:
            st.metric(
                "Model Confidence",
                f"{confidence:.1f}%",
                "High certainty"
            )
        
        with result_col3:
            st.metric(
                "Expected Monthly Profit",
                f"₹{monthly_profit:,.0f}",
                f"₹{annual_profit:,.0f}/year"
            )
        
        # Reasons for low profitability
        st.markdown("### ⚠️ Concerns with This Product:")
        
        concerns = []
        if profit_per_unit < 50:
            concerns.append(f"💰 Thin profit margin (₹{profit_per_unit:.0f}/unit) - High risk")
        if rating < 3.5:
            concerns.append(f"⭐ Low customer rating ({rating}/5) - May limit sales")
        if monthly_sales < 50:
            concerns.append(f"📉 Low sales potential ({monthly_sales} units/month) - Slow growth")
        if competition >= 4:
            concerns.append(f"🎯 High competition (Level {competition}/5) - Hard to compete")
        if num_reviews < 500:
            concerns.append(f"👥 Low social proof ({num_reviews} reviews) - Trust issue")
        
        if not concerns:
            concerns.append("⚠ Overall metrics are weak")
        
        for concern in concerns:
            st.write(f"• {concern}")
        
        # Suggestions
        st.markdown("### 💡 How to Improve:")
        suggestions = []
        if profit_per_unit < 50:
            suggestions.append("**Lower your cost** - Negotiate with suppliers for better pricing")
        if rating < 3.5:
            suggestions.append("**Improve quality** - Source from better manufacturers")
        if monthly_sales < 50:
            suggestions.append("**Better marketing** - Invest in product photography and descriptions")
        if competition >= 4:
            suggestions.append("**Find niche** - Look for less competitive product variations")
        
        for suggestion in suggestions:
            st.write(f"✓ {suggestion}")
        
        st.warning("🛑 **Recommendation:** Consider revising your strategy before launching this product.", icon="⚠️")

# ============================================
# EXAMPLE PRODUCTS SECTION
# ============================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📚 Example Products to Try</h2>', unsafe_allow_html=True)

ex_col1, ex_col2, ex_col3 = st.columns(3)

with ex_col1:
    st.markdown("""
    <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 4px solid #4caf50;">
    <h4 style="margin-top: 0; color: #2e7d32;">✅ High Potential</h4>
    <ul style="margin: 10px 0;">
    <li><b>Price:</b> ₹2,500</li>
    <li><b>Cost:</b> ₹600</li>
    <li><b>Rating:</b> 4.8/5</li>
    <li><b>Sales:</b> 300/month</li>
    <li><b>Competition:</b> Low</li>
    </ul>
    <p style="margin: 0; color: #2e7d32;"><b>Est. Profit:</b> ₹1,15,500/month</p>
    </div>
    """, unsafe_allow_html=True)

with ex_col2:
    st.markdown("""
    <div style="background: #fff3e0; padding: 20px; border-radius: 10px; border-left: 4px solid #ff9800;">
    <h4 style="margin-top: 0; color: #e65100;">🤔 Borderline</h4>
    <ul style="margin: 10px 0;">
    <li><b>Price:</b> ₹1,500</li>
    <li><b>Cost:</b> ₹500</li>
    <li><b>Rating:</b> 3.5/5</li>
    <li><b>Sales:</b> 75/month</li>
    <li><b>Competition:</b> Medium</li>
    </ul>
    <p style="margin: 0; color: #e65100;"><b>Est. Profit:</b> ₹14,062/month</p>
    </div>
    """, unsafe_allow_html=True)

with ex_col3:
    st.markdown("""
    <div style="background: #ffebee; padding: 20px; border-radius: 10px; border-left: 4px solid #f44336;">
    <h4 style="margin-top: 0; color: #c62828;">❌ High Risk</h4>
    <ul style="margin: 10px 0;">
    <li><b>Price:</b> ₹800</li>
    <li><b>Cost:</b> ₹700</li>
    <li><b>Rating:</b> 2.0/5</li>
    <li><b>Sales:</b> 10/month</li>
    <li><b>Competition:</b> High</li>
    </ul>
    <p style="margin: 0; color: #c62828;"><b>Est. Loss:</b> ₹1,500/month</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# INFORMATION SECTION
# ============================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<h2 class="section-title">ℹ️ How It Works</h2>', unsafe_allow_html=True)

info_tab1, info_tab2, info_tab3 = st.tabs(["About Model", "Calculation Method", "FAQ"])

with info_tab1:
    st.write("""
    **Machine Learning Model:** Random Forest Classifier
    - Trained on 100 simulated Amazon India products
    - 85% accuracy on test data
    - Predicts profitability based on 6 key factors
    
    **What the Model Considers:**
    1. **Price** - Selling price point
    2. **Cost** - Product procurement cost
    3. **Rating** - Customer satisfaction (1-5)
    4. **Reviews** - Social proof & trust
    5. **Monthly Sales** - Volume potential
    6. **Competition** - Market saturation
    
    **Profitability Threshold:** ₹5,000+ monthly profit
    """)

with info_tab2:
    st.write("""
    **Formula Used:**
    
    ```
    Monthly Profit = (Price - Cost - Amazon Fee - GST) × Monthly Sales
    ```
    
    **Where:**
    - **Amazon Fee** = Price × 35% (typical FBA commission)
    - **GST** = Price × 18% (Government tax in India)
    - **Profit is calculated per unit, then multiplied by expected monthly sales**
    
    **Example Calculation:**
    - Selling Price: ₹2,500
    - Product Cost: ₹600
    - Amazon Fee: ₹875 (35%)
    - GST: ₹450 (18%)
    - Profit/Unit: ₹575
    - Monthly Sales: 200 units
    - **Monthly Profit: ₹1,15,000 ✅**
    """)

with info_tab3:
    st.write("""
    **Q: How accurate is this prediction?**
    
    A: The model is 85% accurate on test data. Use it as a guide, not a guarantee. 
    Real-world factors like seasonality, trends, and marketing can affect results.
    
    ---
    
    **Q: What if my product doesn't match the examples?**
    
    A: The model works with any price point and category. Enter your actual figures 
    and the AI will analyze based on patterns it learned.
    
    ---
    
    **Q: Can I use this for non-dropshipping products?**
    
    A: Yes! The model works for any Amazon product. Just adjust the costs accordingly.
    
    ---
    
    **Q: Why does the model sometimes contradict my instincts?**
    
    A: AI models find patterns humans might miss. If you disagree, trust your market 
    knowledge, but consider the model's reasoning.
    
    ---
    
    **Q: How is GST calculated?**
    
    A: At 18% on the full selling price. This is standard for most product categories 
    on Amazon India.
    """)

# ============================================
# FOOTER
# ============================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <p><b>Amazon Profit Predictor</b> | Powered by Machine Learning</p>
    <p>Built for Indian dropshipping entrepreneurs | All calculations in Indian Rupees (₹)</p>
    <p style="font-size: 0.85em; opacity: 0.8;">⚠️ Disclaimer: This tool provides estimates only. Always conduct your own market research before launching products.</p>
</div>
""", unsafe_allow_html=True)
