import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os, sys

# Load modules
sys.path.append("modules")
from data_analyzer import DataAnalyzer
from text_analyzer import TextAnalyzer
from image_analyzer import ImageAnalyzer
from ai_engine import DataInsightGenerator, TextInsightGenerator, ImageInsightGenerator


# ===========================
# 🎨 BEAUTIFUL PAGE CONFIG
# ===========================
st.set_page_config(page_title="Smart Insight Engine",  layout="wide")

st.markdown("""
    <h1 style='text-align:center; color:#2C73D2;'>
         Smart Insight Engine
    </h1>
    <p style='text-align:center; color:gray; font-size:17px;'>
        One Engine. Unlimited Insights.
    </p>
    <hr>
""", unsafe_allow_html=True)


# ===========================
# 🎛️ SIDEBAR
# ===========================
with st.sidebar:
    st.markdown("### 🎯 Choose Analysis Mode")
    mode = st.radio("", ["📊 Data Analysis (CSV)", "📝 Text Analysis", "🖼️ Image Analysis"])

    st.markdown("---")
    st.markdown("### 🤖 AI Settings")
    use_ai = st.checkbox("Enable AI Insights", True)

    ai_provider = st.selectbox("AI Engine", ["Mock (Free)", "Google Gemini"])
    provider_map = {"Mock (Free)": "mock", "Google Gemini": "gemini"}

    st.markdown("<hr>", unsafe_allow_html=True)


# ===========================
# 🤖 Helper
# ===========================
def run_ai(gen, content):
    with st.spinner("AI Thinking..."):
        try:
            return gen(content)
        except Exception as e:
            st.error(f"AI Error: {e}")
            return None


# ===========================
# 📊 DATA ANALYSIS
# ===========================
if "Data Analysis" in mode:

    st.subheader("📂 Upload CSV File")
    file = st.file_uploader(" ", type="csv")

    if file:
        path = f"uploads/{file.name}"
        os.makedirs("uploads", exist_ok=True)
        with open(path, "wb") as f: f.write(file.getbuffer())

        analyzer = DataAnalyzer(path)

        if analyzer.load_data():
            df = analyzer.df

            # Metrics section
            st.markdown("### 📈 Dataset Overview")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Rows", len(df))
            col2.metric("Columns", len(df.columns))
            col3.metric("Missing", df.isnull().sum().sum())
            col4.metric("Size", f"{df.memory_usage().sum()/1024**2:.2f} MB")

            tab1, tab2, tab3, tab4 = st.tabs(
                ["📋 Preview", "📊 Statistics", "📈 Visualization", "🤖 AI Insights"]
            )

            with tab1:
                st.dataframe(df.head())

            with tab2:
                st.dataframe(df.describe())

            with tab3:
                nums = df.select_dtypes("number").columns
                if len(nums) > 0:
                    col = st.selectbox("Choose Column", nums)
                    st.plotly_chart(px.histogram(df, x=col))

            with tab4:
                if use_ai and st.button("Generate Insights"):
                    info = analyzer.get_info()
                    ai = DataInsightGenerator(provider_map[ai_provider])
                    st.info(ai.analyze_dataset(info))


# ===========================
# 📝 TEXT ANALYSIS
# ===========================
elif "Text Analysis" in mode:

    st.subheader("📝 Enter Text")
    text = st.text_area("", height=200)

    if len(text) > 10 and st.button("Analyze Text"):
        analyzer = TextAnalyzer(text)

        tab1, tab2, tab3, tab4 = st.tabs(
            ["📊 Statistics", "😊 Sentiment", "🔑 Keywords", "🤖 AI Insights"]
        )

        with tab1: st.write(analyzer.get_basic_stats())
        with tab2: st.write(analyzer.sentiment_analysis())
        with tab3: st.write(analyzer.extract_keywords(15))

        with tab4:
            if use_ai and st.button("AI Enhance"):
                ai = TextInsightGenerator(provider_map[ai_provider])
                summary = analyzer.extractive_summary(3)
                st.info(ai.enhance_summary(text, summary))


# ===========================
# 🖼️ IMAGE ANALYSIS
# ===========================
elif "Image Analysis" in mode:

    st.subheader("🖼️ Upload Image")
    file = st.file_uploader(" ", type=["png", "jpg", "jpeg"])

    if file:
        img = Image.open(file)
        st.image(img, use_column_width=True)

        path = f"uploads/{file.name}"
        img.save(path)

        if st.button("Analyze Image"):
            analyzer = ImageAnalyzer(path)
            results = analyzer.full_analysis()

            tab1, tab2, tab3 = st.tabs(["📋 Metadata", "🎨 Colors", "🤖 AI Insights"])

            with tab1: st.json(results["metadata"])
            with tab2: st.json(results["color_analysis"])

            with tab3:
                if use_ai and st.button("AI Vision Insights"):
                    ai = ImageInsightGenerator(provider_map[ai_provider])
                    st.info(ai.interpret_image_analysis(results))


# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Made by Riona Gonsalves")
