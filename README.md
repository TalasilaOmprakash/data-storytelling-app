# 📊 Smart Data Storytelling App

A dynamic and intelligent data analysis application built using Streamlit that works with **any CSV dataset** and automatically generates insights, visualizations, and trends.

---

## 🚀 Features

### 🔍 Smart Data Handling
- Supports any CSV file
- Handles encoding issues (UTF-8, Latin1, CP1252)
- Automatically detects numeric and categorical columns
- Ignores ID columns for meaningful analysis

---

### 🧠 Intelligent Analysis
- Auto-selects the most relevant metric
- Detects dataset type:
  - 🩺 Health datasets (e.g., diabetes)
  - 💰 Sales datasets
  - 🎬 Movie datasets
  - 📦 Generic datasets

---

### 📊 Visualizations
- Top category analysis
- Trend analysis (supports Date or YEAR + MONTH)
- Correlation heatmap
- Custom column exploration

---

### 🤖 AI-Style Insights
- Automatically generates human-like insights
- Detects:
  - Trends 📈
  - Variability 📊
  - Negative values ⚠️
  - Top & low-performing categories 🏆

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- Matplotlib
- Seaborn

---

## ▶️ How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
