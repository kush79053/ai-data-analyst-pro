# Core libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# New OpenAI setup
from openai import OpenAI
import os

# PDF generator
from fpdf import FPDF

# Initialize OpenAI client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page config
st.set_page_config(page_title="AI Data Analyst Pro", layout="wide")

# Title
st.title("🤖 AI Data Analyst Pro")

st.write("Upload your dataset to generate insights, visuals, and AI analysis")

# File upload
file = st.file_uploader("Upload CSV", type=["csv"])

# Run app only if file is uploaded
if file:
    df = pd.read_csv(file)

    # Safety check
    if df.empty:
        st.error("Dataset is empty")
        st.stop()

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "📈 Visuals", 
        "🤖 AI Insights", 
        "💬 Chat"
    ])

    # -------- TAB 1: Overview --------
    with tab1:
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        st.subheader("Statistics")
        st.write(df.describe())

        st.subheader("Missing Values")
        st.write(df.isnull().sum())

    # -------- TAB 2: Visuals --------
    with tab2:
        st.subheader("Auto Visualization")

        # Heatmap with numeric-only columns
        if st.button("Generate Correlation Heatmap"):
            numeric_df = df.select_dtypes(include='number')

            if numeric_df.shape[1] < 2:
                st.warning("Not enough numeric columns for correlation")
            else:
                plt.figure(figsize=(8,5))
                sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
                st.pyplot(plt)

        st.subheader("Custom Chart")

        col1 = st.selectbox("Select Column 1", df.columns)
        col2 = st.selectbox("Select Column 2", df.columns)

        if st.button("Generate Scatter Plot"):
            try:
                plt.figure()
                sns.scatterplot(x=df[col1], y=df[col2])
                st.pyplot(plt)
            except Exception as e:
                st.error(f"Error generating plot: {e}")

    # -------- TAB 3: AI Insights --------
    with tab3:
        st.subheader("AI Business Insights")

        if st.button("Generate Insights"):
            try:
                prompt = f"""
                You are a senior data analyst working in a consulting firm like EXL.
                Analyze the dataset summary below and provide:
                1. Key trends
                2. Business insights
                3. Actionable recommendations
                
                Data Summary:
                {df.describe().to_string()}
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )

                insights = response.choices[0].message.content
                st.write(insights)

                st.session_state["insights"] = insights

            except Exception as e:
                st.error(f"AI Error: {e}")

    # -------- TAB 4: Chat --------
    with tab4:
        st.subheader("Chat with your Data")

        question = st.text_input("Ask something about your dataset")

        if question:
            try:
                prompt = f"""
                You are a data analyst.
                Dataset sample:
                {df.head().to_string()}
                
                Question: {question}
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )

                st.write(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Chat Error: {e}")

    # -------- PDF Report --------
    st.subheader("📄 Download AI Report")

    if st.button("Generate PDF Report"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="AI Data Analysis Report", ln=True)

            if "insights" in st.session_state:
                pdf.multi_cell(0, 10, st.session_state["insights"])
            else:
                pdf.multi_cell(0, 10, "No insights generated yet.")

            pdf.output("report.pdf")

            with open("report.pdf", "rb") as f:
                st.download_button("Download Report", f, file_name="AI_Report.pdf")

        except Exception as e:
            st.error(f"PDF Error: {e}")
