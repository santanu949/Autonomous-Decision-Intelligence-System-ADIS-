# Autonomous Decision Intelligence System (ADIS)

ADIS is a production-grade Decision Intelligence platform designed to transform raw, unstructured data into validated insights, justified decisions, and actionable recommendations. Built for modern enterprise needs, it provides a rigorous analytical pipeline that surfaces high-confidence guidance with complete explainability.

## 🚀 Key Features

- **Intelligent Ingestion:** Adaptive parsing of JSON/CSV data with automatic type inference and quality profiling.
- **Multi-Method Analysis:** Rigorous analytical pipeline including statistical profiling, anomaly detection (Z-score, IQR, MAD), and correlation testing.
- **Machine Learning Engine:** Automated forecasting (Linear Regression) and data segmentation (K-Means++ Clustering).
- **Decision Synthesis:** Multi-signal reasoning engine that weighs business heuristics against analytical results.
- **Explainability First:** Dual-level explanations (Executive Summary & Technical Detail) with full reasoning chains and factor breakdowns.
- **Interactive Dashboard:** Modern React interface with real-time visualization, confidence gauges, and scenario simulations.
- **Conversational AI:** Integrated chat layer to query analysis results using natural language.

## 🏗 System Architecture

ADIS follows a modular, decoupled architecture:
1. **Frontend (React 18):** A "Decision-First" UI built with TailwindCSS and Recharts for maximum visual clarity and responsiveness.
2. **Backend (FastAPI):** High-performance Python API that orchestrates the data-to-decision pipeline.
3. **Analytical Pipeline:** A series of isolated modules (Ingestion → Analysis → ML → Synthesis → Explainability) that process data sequentially.
4. **Data Flow:** Raw Data Input → Validation/Quality Check → Multi-Signal Analysis → ML Forecasting → Decision Synthesis → Human-Readable Explanation.

## 💻 Tech Stack

- **Frontend:** React 18, TailwindCSS, Recharts, Lucide Icons, Craco.
- **Backend:** Python 3.10+, FastAPI, Pydantic, Scikit-learn, Pandas, NumPy.
- **Database:** MongoDB (Audit Trail & History).
- **Ops:** Docker, Docker Compose, Kubernetes, Prometheus.

## ⚙️ Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/santanu949/Autonomous-Decision-Intelligence-System-ADIS-.git
cd Autonomous-Decision-Intelligence-System-ADIS-
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/scripts/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your MongoDB credentials if needed
python server.py
```

### 3. Frontend Setup
```bash
cd ../frontend
yarn install  # or npm install
npm start
```

## 📖 Usage Guide

1. **Dashboard:** Upload your dataset (JSON or CSV) via the Home page.
2. **Analysis:** Click "Analyze" to run the full ADIS pipeline.
3. **Review Results:**
   - **Confidence Gauge:** See the AI's overall confidence in the current recommendations.
   - **Factor Breakdown:** Understand which variables most influenced the decisions.
   - **Interactive Chat:** Ask questions like "Why did you recommend restocking?" or "What are the key trends?".
4. **Simulation:** Use the Scenario Simulation tool in the Analytics tab to test "What-if" variables.

## 📂 Project Structure

```text
├── backend/
│   ├── core/           # Pipeline Orchestrator & Models
│   ├── ingestion/      # Data Parsing & Validation
│   ├── analytics/      # Stats, Anomaly, Correlation, Trends
│   ├── ml/             # Forecasting & Clustering
│   ├── decisions/      # Reasoning & Synthesis
│   ├── explainability/ # Explanation Generation
│   └── server.py       # FastAPI Application
├── frontend/
│   ├── src/
│   │   ├── components/ # UI Layouts & Widgets
│   │   ├── pages/      # Home, Analytics, Reports, etc.
│   │   └── services/   # API Communication Layer
└── k8s/                # Kubernetes Deployment Manifests
```

## 🔮 Future Improvements

- **Advanced ML:** Integration of LSTM/GRU for deeper time-series forecasting.
- **Real-Time Integration:** Streaming data support via WebSockets or Kafka.
- **Enterprise Security:** Full OAuth2/SSO integration and RBAC (Role-Based Access Control).
- **Enhanced Simulations:** Monte Carlo simulations for probabilistic risk assessment.

## 🖥 UI Description

The ADIS interface is designed with a **clean, dark-mode-first aesthetic** utilizing Indigo and Slate color palettes. 
- **Navigation:** A floating curved navbar providing quick access to Dashboard, Analytics, and Reports.
- **Decision Cards:** Prominent cards displaying "Actions" with associated confidence levels and color-coded risk indicators.
- **Visualizations:** Interactive area and bar charts showing multi-variable trends and ML predictions.
- **Analytical Depth:** Collapsible technical breakdowns for users who need to see the "under the hood" logic.

---
© 2026 ADIS Team. All rights reserved.
