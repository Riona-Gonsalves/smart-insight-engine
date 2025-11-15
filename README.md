# 🧠 Smart Insight Engine

AI-Powered Multi-Modal Data Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Overview

Smart Insight Engine is a comprehensive data analysis platform that combines:
- 📊 **CSV Data Analysis** - Automated cleaning, statistics, and visualization
- 📝 **Text Analysis** - Sentiment analysis, keyword extraction, and summarization
- 🖼️ **Image Analysis** - OCR, color analysis, and edge detection
- 🤖 **AI-Powered Insights** - Integration with OpenAI and Google Gemini

## ✨ Features

### Data Analysis
- Automatic encoding detection for CSV files
- Statistical summaries and correlation matrices
- Interactive visualizations (histograms, box plots, heatmaps)
- Outlier detection and trend analysis

### Text Analysis
- Sentiment analysis with polarity scoring
- Keyword extraction and frequency analysis
- Automatic text summarization
- Readability scoring (Flesch-Kincaid)

### Image Analysis
- OCR text extraction using Tesseract
- Color analysis and brightness detection
- Edge detection and complexity analysis
- Image metadata extraction

### AI Integration
- Mock mode for testing without API costs
- OpenAI GPT integration for advanced insights
- Google Gemini API support
- Customizable AI prompts

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Tesseract OCR (for image text extraction)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/smart-insight-engine.git
cd smart-insight-engine
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download NLTK data**
```bash
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords')"
```

5. **Set up environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys (optional)
```

6. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Tech Stack

- **Frontend:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly, Matplotlib, Seaborn
- **NLP:** NLTK, TextBlob
- **Computer Vision:** OpenCV, PIL, Tesseract
- **AI APIs:** OpenAI, Google Gemini

## 📁 Project Structure
```
smart-insight-engine/
├── modules/
│   ├── data_analyzer.py      # CSV analysis
│   ├── text_analyzer.py      # Text processing
│   ├── image_analyzer.py     # Image analysis
│   └── ai_engine.py          # AI integration
├── data/                     # Sample data files
├── uploads/                  # User uploaded files
├── app.py                    # Main Streamlit app
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

## 📊 Usage Examples

### Data Analysis
1. Upload a CSV file
2. View automatic statistics and visualizations
3. Generate AI insights with one click

### Text Analysis
1. Paste or upload text
2. View sentiment analysis and keywords
3. Get AI-enhanced summaries

### Image Analysis
1. Upload an image
2. Extract text with OCR
3. Analyze colors and structure

## 🔑 API Keys (Optional)

The app works in **mock mode** without API keys. To use real AI:

1. **OpenAI:** Get key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. **Google Gemini:** Get key from [makersuite.google.com](https://makersuite.google.com/app/apikey)
3. Add to `.env` file

