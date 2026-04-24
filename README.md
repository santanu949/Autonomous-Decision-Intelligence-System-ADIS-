# 🧠 ADIS: Autonomous Decision Intelligence System

[![FastAPI](https://img.shields.io/badge/FastAPI-005571.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A.svg?logo=react&logoColor=61DAFB)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5.svg?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Status](https://img.shields.io/badge/Status-Advanced_Prototype-orange.svg)]()

**ADIS** is a production-grade Decision Intelligence platform designed to transform messy, complex datasets into clear, strategic action plans. Unlike traditional dashboards that only visualize data, ADIS analyzes, predicts, and recommends the next best move for your business.

---

## 📖 Overview

In today's data-driven world, the challenge isn't having data—it's knowing what to do with it. **ADIS (Autonomous Decision Intelligence System)** solves this by acting as a "Digital Super Manager." It ingests raw data, identifies anomalies, predicts future trends using machine learning, and synthesizes these findings into plain-English strategic recommendations.

### The Core Idea
ADIS doesn't just show you "What" happened; it explains "Why" it happened and tells you "What" to do next. It bridges the gap between complex data science and intuitive business leadership.

---

## ✨ Key Features

- **🧼 Autonomous Data Ingestion**: Automatically handles data cleaning, parsing, and normalization of CSV/JSON files.
- **🔮 Predictive Intelligence**: Integrated Machine Learning models that forecast future outcomes based on historical patterns.
- **🕵️ Anomaly & Outlier Detection**: Spots "weird" data points or potential risks before they become critical issues.
- **💡 AI Reasoning Engine**: Translates complex mathematical models into human-readable logic and "Action Plans."
- **💬 Conversational Data AI**: A built-in chat interface that allows you to "talk" to your data using natural language.
- **📊 Decision-First UI**: A premium dashboard focused on "Strategic Actions" rather than just static charts.
- **🚀 Cloud-Native Architecture**: Fully containerized and ready for orchestration via Kubernetes and monitoring via Prometheus.

---

## 🏗 System Architecture

The ADIS pipeline follows a high-performance "Factory" model:

1.  **Ingestion & Parsing**: Raw data is loaded and structured by the backend.
2.  **Analytics Engine**: Statistical analysis identifies correlations and trends.
3.  **ML Prediction**: Scikit-Learn models generate forecasts and confidence scores.
4.  **Strategic Synthesis**: The reasoning engine combines all insights into a final "Decision."
5.  **Interactive Dashboard**: The React frontend displays the final strategy and interactive visualizations.

---

## 🛠 Tech Stack

### Backend (The Brain)
- **Framework**: FastAPI (Python)
- **Data Science**: Pandas, NumPy
- **Machine Learning**: Scikit-Learn
- **Database**: MongoDB

### Frontend (The Visuals)
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **Visualization**: Recharts, Framer Motion

### Infrastructure (The Scale)
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes (k8s)
- **Monitoring**: Prometheus & Grafana

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker (optional, for containerized setup)

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/santanu949/Autonomous-Decision-Intelligence-System.git
   cd Autonomous-Decision-Intelligence-System
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   python server.py
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   npm run start
   ```

4. **Access the Platform**
   Open `http://localhost:3000` to view the dashboard.

---

## 📖 Usage

1. **Upload Data**: Navigate to the upload section and provide your dataset.
2. **Run Analysis**: Trigger the autonomous pipeline to process the data.
3. **Review Strategy**: Read the "Strategic Action" at the top of the dashboard.
4. **Interact with AI**: Use the bottom-right chat bubble to ask specific questions about your data.

---

## 🛠 Project Status

This project is currently an **Advanced Prototype**. 
- [x] Core Analysis Pipeline
- [x] ML Prediction Engine
- [x] AI Chat Integration
- [ ] Real-time External Data Connectors (In Progress)
- [ ] Multi-User Governance (Roadmap)

---

## 📄 License

This project is licensed under the MIT License.

---

*Developed by [Santanu Samanta](https://github.com/santanu949) — Empowering data-driven leadership.*
