
# 🤖 AI Data Analyst Pro

An AI-powered data analysis web app built with *Streamlit* and *GPT-4o-mini*. Upload any CSV dataset and instantly get statistical summaries, visualizations, AI-generated business insights, and an interactive chat interface — all in one place.

---

## Features

- *📊 Dataset Overview* — Preview your data, descriptive statistics, and missing value counts at a glance
- *📈 Auto Visualizations* — Generate correlation heatmaps and custom scatter plots with a single click
- *🤖 AI Business Insights* — GPT-4o-mini analyzes your dataset and returns key trends, business insights, and actionable recommendations
- *💬 Chat with Your Data* — Ask natural language questions about your dataset and get instant AI responses
- *📄 PDF Report Export* — Download a PDF report of the AI-generated insights

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Streamlit | Web app frontend |
| Pandas | Data loading & processing |
| Matplotlib / Seaborn | Data visualization |
| OpenAI (GPT-4o-mini) | AI insights & chat |
| FPDF | PDF report generation |

---

## Getting Started

### 1. Clone the repo

bash
git clone https://github.com/kush79053/ai-data-analyst-pro.git
cd ai-data-analyst-pro


### 2. Install dependencies

bash
pip install -r requirements.txt


### 3. Set your OpenAI API key

bash
export OPENAI_API_KEY="your-api-key-here"


### 4. Run the app

bash
streamlit run app.py


---

## How to Use

1. Upload a .csv file using the file uploader
2. Explore the *Overview* tab for stats and missing values
3. Go to *Visuals* to generate a correlation heatmap or custom scatter plot
4. Click *Generate Insights* in the *AI Insights* tab for GPT-powered analysis
5. Use the *Chat* tab to ask specific questions about your data
6. Download a *PDF Report* of the insights

---

## Project Structure


ai-data-analyst-pro/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md


---

## Requirements


streamlit
pandas
matplotlib
seaborn
openai
fpdf


---

## Author

*Kushagra* — [GitHub](https://github.com/kush79053)

---

> Built as part of a data science portfolio. Demonstrates integration of LLMs with traditional data analysis workflows.
