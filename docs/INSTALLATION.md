# Installation Guide

## Prerequisites
- Python 3.8 or higher
- Tesseract OCR (optional, for image text extraction)

## Quick Install

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/smart-insight-engine.git
cd smart-insight-engine
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download NLTK data:
```bash
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords')"
```

5. Set up environment:
```bash
copy .env.example .env
# Edit .env with your API keys
```

6. Run the app:
```bash
streamlit run app.py
```

## Tesseract OCR (Optional)

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

**Mac:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```