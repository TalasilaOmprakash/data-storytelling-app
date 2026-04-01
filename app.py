import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Smart Data Storytelling App", layout="wide")

st.title("📊 Smart Data Storytelling App")

# ================= FILE UPLOAD =================
file = st.file_uploader("Upload your CSV file", type=["csv"])

# ================= SAFE LOADER =================
@st.cache_data
def load_data(file):
    try:
        return pd.read_csv(file, encoding="utf-8", encoding_errors="ignore")
    except:
        try:
            return pd.read_csv(file, encoding="latin1", encoding_errors="ignore")
        except:
            return pd.read_csv(file, encoding="cp1252", encoding_errors="ignore")

if file is not None:

    df = load_data(file)

    if df.empty:
        st.error("Empty dataset")
        st.stop()

    # ================= PREVIEW =================
    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # ================= INFO =================
    st.subheader("📊 Dataset Info")
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # ================= DATASET TYPE DETECTION =================
    dataset_type = "generic"

    columns_joined = " ".join(df.columns).upper()

    if "OUTCOME" in columns_joined:
        dataset_type = "health"
    elif "SALES" in columns_joined:
        dataset_type = "sales"
    elif "BUDGET" in columns_joined or "BOXOFFICE" in columns_joined:
        dataset_type = "movie"

    st.write(f"🧠 Detected Dataset Type: **{dataset_type.upper()}**")

    # ================= COLUMN TYPES =================
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    # REMOVE ID COLUMNS
    def is_id(col):
        return "id" in col.lower() or df[col].nunique() == len(df)

    numeric_cols = [c for c in numeric_cols if not is_id(c)]

    st.subheader("🔍 Clean Column Types")
    st.write("Numeric:", numeric_cols)
    st.write("Categorical:", categorical_cols)

    if not numeric_cols:
        st.warning("No meaningful numeric columns found")
        st.stop()

    # ================= SMART METRIC =================
    metric_col = df[numeric_cols].var().idxmax()

    st.subheader("💰 Key Metric (Auto Selected)")
    st.write(f"Selected Metric: **{metric_col}**")

    st.metric("Total", round(df[metric_col].sum(), 2))
    st.metric("Average", round(df[metric_col].mean(), 2))

    # ================= NEGATIVE CHECK =================
    if (df[metric_col] < 0).any():
        st.warning(f"⚠️ Negative values detected in {metric_col}")

    # ================= CATEGORY =================
    best_cat = None
    for col in categorical_cols:
        if df[col].nunique() < 50:
            best_cat = col
            break

    st.subheader("📊 Top Categories by Metric")

    if best_cat:
        chart = df.groupby(best_cat)[metric_col].sum().sort_values(ascending=False).head(10)
        st.bar_chart(chart)
    else:
        st.info("No suitable categorical column found")

    # ================= TREND =================
    st.subheader("📅 Trend Analysis")

    try:
        if "YEAR" in df.columns and "MONTH" in df.columns:
            df["DATE"] = pd.to_datetime(df["YEAR"].astype(str) + "-" + df["MONTH"].astype(str) + "-01")
            trend = df.groupby("DATE")[metric_col].sum()
            st.line_chart(trend)

        else:
            date_cols = [c for c in df.columns if "date" in c.lower()]
            if date_cols:
                dcol = date_cols[0]
                df[dcol] = pd.to_datetime(df[dcol], errors="coerce")
                trend = df.groupby(df[dcol].dt.to_period("M"))[metric_col].mean()
                trend.index = trend.index.astype(str)
                st.line_chart(trend)
            else:
                st.info("No time-based column found")

    except:
        st.warning("Trend analysis failed")

    # ================= DOMAIN-SPECIFIC ANALYSIS =================

    # 🩺 HEALTH
    if dataset_type == "health":
        st.subheader("🩺 Health Analysis")

        st.bar_chart(df["Outcome"].value_counts())
        st.dataframe(df.groupby("Outcome").mean())

        for col in ["Glucose", "BMI", "Age"]:
            if col in df.columns:
                st.write(f"{col} vs Outcome")
                st.bar_chart(df.groupby("Outcome")[col].mean())

    # 💰 SALES
    if dataset_type == "sales":
        st.subheader("💰 Sales Analysis")

        if "SUPPLIER" in df.columns and "RETAIL SALES" in df.columns:
            top = df.groupby("SUPPLIER")["RETAIL SALES"].sum().sort_values(ascending=False).head(10)
            st.bar_chart(top)

    # 🎬 MOVIE
    if dataset_type == "movie":
        st.subheader("🎬 Movie Analysis")

        if "BudgetDollars" in df.columns and "BoxOfficeDollars" in df.columns:
            df["Profit"] = df["BoxOfficeDollars"] - df["BudgetDollars"]
            top = df.sort_values("Profit", ascending=False)[["Title", "Profit"]].head(10)
            st.dataframe(top)

    # ================= HEATMAP =================
    if len(numeric_cols) > 1:
        st.subheader("🔥 Correlation Heatmap")
        fig, ax = plt.subplots()
        sns.heatmap(df[numeric_cols].corr(), ax=ax)
        st.pyplot(fig)

    # ================= CUSTOM =================
    st.subheader("🎯 Custom Analysis")

    col = st.selectbox("Choose column", df.columns)

    if col in numeric_cols:
        st.line_chart(df[col].head(1000))
    else:
        st.bar_chart(df[col].value_counts().head(10))

    # ================= FILTER =================
    st.subheader("🔎 Filter Data")

    fcol = st.selectbox("Filter column", df.columns)

    if fcol in categorical_cols:
        val = st.selectbox("Value", df[fcol].dropna().unique())
        st.dataframe(df[df[fcol] == val].head(100))

    # ================= AI INSIGHTS =================
    st.subheader("🤖 AI-Generated Insights")

    insights = []

    insights.append(f"The dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")

    mean_val = df[metric_col].mean()
    max_val = df[metric_col].max()
    min_val = df[metric_col].min()

    insights.append(f"'{metric_col}' has an average of {round(mean_val,2)}, max {round(max_val,2)}, min {round(min_val,2)}.")

    if df[metric_col].std() > mean_val:
        insights.append(f"'{metric_col}' shows high variability.")
    else:
        insights.append(f"'{metric_col}' is relatively stable.")

    if (df[metric_col] < 0).any():
        insights.append("Negative values detected (possible corrections or returns).")

    if best_cat:
        grouped = df.groupby(best_cat)[metric_col].sum()
        insights.append(f"Top {best_cat}: {grouped.idxmax()}")
        insights.append(f"Lowest {best_cat}: {grouped.idxmin()}")

    if "DATE" in df.columns:
        trend = df.groupby("DATE")[metric_col].sum()
        if len(trend) > 1:
            if trend.iloc[-1] > trend.iloc[0]:
                insights.append("Overall increasing trend observed.")
            else:
                insights.append("Trend is decreasing or fluctuating.")

    for insight in insights:
        st.write(f"👉 {insight}")