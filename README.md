# NexaPulse AI — Enterprise Amazon Intelligence & Cross-Border SaaS Platform

NexaPulse AI is an enterprise-grade e-commerce analytics, machine learning, and cross-border intelligence platform engineered for Amazon sellers, dropshippers, and Global Capability Center (GCC) operators managing multi-region brand portfolios across global Amazon marketplaces (United States, Europe, United Kingdom, United Arab Emirates, and India).

---

## Technical Architecture

NexaPulse AI is built on a decoupled full-stack architecture:

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons, Recharts
- **Backend Services**: Python FastAPI, Uvicorn ASGI, Pydantic validation
- **Machine Learning Pipeline**: Scikit-Learn (Random Forest Regressor & Binary Classifier), NumPy, Pandas
- **Integrations**: Amazon Selling Partner API (SP-API) catalog & product fees integration module

---

## Core Capabilities

### 1. GCC Executive Control Tower
- **Consolidated Portfolio Analytics**: Real-time aggregation of Global Revenue, EBITDA Net Profit, and Portfolio Operating Margins.
- **Multi-Currency Engine**: Automated multi-jurisdiction rollup supporting USD ($), INR (₹), EUR (€), GBP (£), and AED.
- **Marketplace Distribution**: Visual revenue & margin allocation across regional operational hubs.

### 2. AI Profit Predictor & Compliance Engine
- **Sales Estimation Engine**: Random Forest Regressor estimating monthly unit sales based on category dynamics, price tier, review volume, and rating.
- **Winner Probability Classifier**: Binary classifier predicting product launch success rates.
- **Amazon Dropshipping Policy Guard**: Seller of Record (SoR) verification indicator and 2-Day Handling SLA warning banner to maintain Late Shipment Rate (LSR) under 4%.

### 3. Cross-Border Logistics & Landed Cost Engine
- **Freight Cost Estimator**: Multi-modal shipping calculations covering Sea Freight (LCL/FCL) and Air Express Freight.
- **Landed Cost & Duty Calculator**: Import cost modeling incorporating 6.0% customs tariff duties, 0.5% transit insurance, and local port handling fees.

### 4. Market Research & Keyword Intelligence
- **Black Box Catalog Explorer**: Multi-dimensional attribute filtering across product database tiers.
- **Magnet Semantic Keyword Engine**: Category-Aware Semantic Intent filtering providing search volume, CPC bid estimates, and opportunity scoring.

---

## Repository Structure

```
amazon-profit-predictor/
├── backend.py                   # FastAPI server & REST API routes
├── config.py                    # Fee schedules, tax rates, and exchange rate constants
├── gcc_engine.py                # Cross-border landed cost & currency conversion engine
├── amazon_sp_api_client.py      # Amazon Selling Partner API (SP-API) client interface
├── data_generator.py            # Real-world brand product catalog generator
├── model_trainer.py             # Random Forest machine learning pipeline
├── app.py                       # Streamlit fallback entrypoint
├── products.csv                 # Product catalog dataset
├── sales_model.pkl              # Trained monthly sales regressor model
├── classifier_model.pkl         # Trained profitability classifier model
├── scaler.pkl                   # Trained StandardScaler artifact
├── requirements.txt             # Python dependencies
└── frontend/                    # React single-page web application
    ├── src/
    │   ├── App.jsx              # Main routing & layout container
    │   └── components/          # Dashboard & analytical components
    ├── dist/                    # Compiled production UI bundle
    └── package.json             # Frontend dependencies & build configuration
```

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+ (for frontend development)

### 1. Environment Setup

```bash
git clone https://github.com/shrinithisk/amazon-profit-predictor.git
cd amazon-profit-predictor

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Dataset Generation & Model Training

```bash
# Generate product catalog dataset
python data_generator.py

# Train ML models
python model_trainer.py
```

### 3. Application Launch

#### Production Server (FastAPI + Embedded React Frontend)
```bash
uvicorn backend:app --host 0.0.0.0 --port 8000
```
Access the application at `http://localhost:8000`.

#### Frontend Development Mode
```bash
cd frontend
npm install
npm run dev
```

---

## License

MIT License.
