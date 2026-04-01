# Import required libraries
import streamlit as st              # For building the web app UI
import pandas as pd                # For data manipulation
import matplotlib.pyplot as plt    # For plotting charts
import seaborn as sns              # For advanced visualizations
import openai                      # For using LLM (AI insights)
from fpdf import FPDF              # For generating PDF reports

# Set OpenAI API key (Replace with environment variable in production)
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure Streamlit page
st.set_page_config(page_title="AI Data Analyst Pro", layout="wide")

# App title
st.title("🤖 AI Data Analyst Pro")

# File uploader (only CSV files allowed)
file = st.file_uploader("Upload CSV", type=["csv"])

# If file is uploaded
if file:
    # Read dataset into pandas dataframe
    df = pd.read_csv(file)

    # Create tabs for better UI separation
    tab1, tab2, tab3, tab4 = st.tabs([
        "Overview,Visuals,AI Insights,Chat"
    ])

    # ---------------- TAB 1: DATA OVERVIEW ----------------
    with tab1:
        st.subheader("Dataset Preview")
        st.dataframe(df.head())  # Show first 5 rows

        st.subheader("Statistics")
        st.write(df.describe())  # Show statistical summary

        st.subheader("Missing Values")
        st.write(df.isnull().sum())  # Show missing values count

    # ---------------- TAB 2: VISUALIZATION ----------------
    with tab2:
        st.subheader("Auto Visualization")

        # Generate correlation heatmap
        if st.button("Generate Correlation Heatmap"):
            plt.figure(figsize=(8,5))
            sns.heatmap(df.select_dtypes(include='number').corr(), annot=True, cmap="coolwarm")
            st.pyplot(plt)

        st.subheader("Custom Chart")

        # Dropdowns to select columns
        col1 = st.selectbox("Select Column 1", df.columns)
        col2 = st.selectbox("Select Column 2", df.columns)

        # Generate scatter plot based on selected columns
        if st.button("Generate Scatter Plot"):
            plt.figure()
            sns.scatterplot(x=df[col1], y=df[col2])
            st.pyplot(plt)

    # ---------------- TAB 3: AI INSIGHTS ----------------
    with tab3:
        st.subheader("AI Business Insights")

        # Generate AI insights using LLM
        if st.button("Generate Insights"):
            prompt = f"""
            You are a senior data analyst working in a consulting firm like EXL.
            Analyze the dataset summary below and provide:
            1. Key trends
            2. Business insights
            3. Actionable recommendations
            
            Data Summary:
            {df.describe().to_string()}
            """

            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            # Extract response text
            insights = response['choices'][0]['message']['content']
            st.write(insights)

            # Store insights for PDF generation
            st.session_state["insights"] = insights

    # ---------------- TAB 4: CHAT WITH DATA ----------------
    with tab4:
        st.subheader("Chat with your Data")

        # Input question from user
        question = st.text_input("Ask something about your dataset")

        if question:
            prompt = f"""
            You are a data analyst.
            Dataset sample:
            {df.head().to_string()}
            
            Question: {question}
            """

            # AI response based on user query
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            st.write(response['choices'][0]['message']['content'])

    # ---------------- PDF REPORT GENERATION ----------------
    st.subheader("📄 Download AI Report")

    if st.button("Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()

        # Set font for PDF
        pdf.set_font("Arial", size=12)

        # Add title
        pdf.cell(200, 10, txt="AI Data Analysis Report", ln=True)

        # Add AI insights if available
        if "insights" in st.session_state:
            pdf.multi_cell(0, 10, st.session_state["insights"])

        # Save PDF file
        pdf.output("report.pdf")

        # Provide download button
        with open("report.pdf", "rb") as f:
            st.download_button("Download Report", f, file_name="AI_Report.pdf")
