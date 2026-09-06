# 🌐 AmzDropship Enterprise GCC | Global Capability Centre Suite

An enterprise-grade Global Capability Centre (GCC) analytics, machine learning, and multi-region e-commerce hub for Amazon sellers, dropshippers, and cross-border brands operating across global marketplaces (**United States 🇺🇸, Europe 🇪🇺, United Kingdom 🇬🇧, United Arab Emirates 🇦🇪, and India 🇮🇳**).

---

## 🌟 Key Features & Enterprise Modules

1. **🌐 GCC Executive Control Tower**:
   - Consolidated global portfolio KPIs (Consolidated Global Revenue, Net Profit EBITDA, Portfolio Margin %, Top Performing Regional Hub).
   - Multi-currency reporting rollup (convert all global metrics to **USD ($), INR (₹), EUR (€), GBP (£), or AED**).
   - Regional contribution bar charts and sales share pie charts.

2. **📈 Multi-Region AI Profit Predictor**:
   - Random Forest Regressor & Classifier models trained on global Amazon marketplace features.
   - Dynamic currency and fee modeling for US, Europe, UK, UAE, and India.
   - Winner probability scoring, profit margin delta analysis, and cost breakdowns.

3. **🚢 Cross-Border Logistics & Landed Cost Engine**:
   - International shipping fee calculations (Sea Freight LCL vs Air Express Freight).
   - Cargo insurance (0.5%) & customs import tariffs (6%) landed cost calculations.
   - Automated conversion to destination currency.

4. **🔍 Global Product Research (Black Box)**:
   - Filter and search 1,000 generated global products across US, EU, UK, UAE, and India.

5. **🔑 Global Keyword Research (Magnet)**:
   - Seed keyword search volumes, CPC bids ($/₹), and magnet opportunity scores.

6. **📝 Listing Optimizer (Scribbles)** & **🧮 FBA vs FBM Calculator**:
   - Real-time Amazon listing SEO scoring and side-by-side logistics fee breakdowns.

---

## 📁 Repository Architecture

```
amazon-profit-predictor/
├── config.py            # Central constants, marketplace fee tables, tax rates, exchange rates
├── gcc_engine.py        # Landed cost, multi-jurisdiction tax, currency conversion, portfolio rollups
├── data_generator.py    # Multi-region synthetic dataset generator (1,000 global products)
├── model_trainer.py     # Random Forest ML pipeline for multi-market sales & winner classification
├── app.py               # Main Streamlit Enterprise GCC Dashboard & Suite
├── products.csv         # Generated product dataset
├── classifier_model.pkl # Trained profitability classifier model
├── sales_model.pkl      # Trained monthly sales regressor model
├── scaler.pkl           # Trained StandardScaler feature scaler
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```

---

## 🚀 Quick Start

### 1. Environment Setup

```bash
git clone https://github.com/shrinithisk/amazon-profit-predictor.git
cd amazon-profit-predictor

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Generate Multi-Region Dataset & Train Global ML Models

```bash
# Generate 1,000 multi-region products
python data_generator.py

# Train Random Forest models with regional features
python model_trainer.py
```

### 3. Launch Streamlit GCC Suite

```bash
streamlit run app.py
```
