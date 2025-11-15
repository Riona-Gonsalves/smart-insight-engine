import json
from typing import Dict

# Try importing Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Gemini not installed (pip install google-generativeai)")


# CONFIG
class Config:
    GEMINI_API_KEY = ""
    AI_MODEL_GEMINI = "gemini-2.0-flash-lite"
    TEMPERATURE = 0.7
    MAX_TOKENS = 1000


class AIEngine:
    """
    AI-powered insight generator
    Supports: Google Gemini and Mock mode
    """

    def __init__(self, provider='gemini', api_key=Config.GEMINI_API_KEY):
        self.provider = provider.lower()
        self.mock_mode = False

        print("\n🤖 Initializing AI Engine (Gemini Only)...")

        if self.provider == "gemini":
            if not GEMINI_AVAILABLE:
                print("   ❌ Gemini library missing → switching to mock mode")
                self.mock_mode = True
            else:
                self.api_key = api_key or Config.GEMINI_API_KEY
                if not self.api_key:
                    print("   ❌ No Gemini API key → MOCK MODE enabled")
                    self.mock_mode = True
                else:
                    genai.configure(api_key=self.api_key)
                    self.model = genai.GenerativeModel(Config.AI_MODEL_GEMINI)
                    print("   ✓ Gemini configured successfully")

        else:
            print("   ❌ Only Gemini supported → MOCK MODE enabled")
            self.mock_mode = True

        if self.mock_mode:
            print("   ℹ️ Running in MOCK MODE (fake responses)\n")

    def generate(self, prompt: str) -> str:
        if self.mock_mode:
            return self._mock_response(prompt)
        return self._call_gemini(prompt)

    def _call_gemini(self, prompt: str) -> str:
        """Real Gemini API call"""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"❌ Gemini Error: {str(e)}"

    def _mock_response(self, prompt: str) -> str:
        pl = prompt.lower()
        if "data" in pl:
            return "📊 Mock Data Insight: Dataset looks clean with interesting correlations."
        if "sentiment" in pl:
            return "😊 Mock Sentiment Insight: The text is positive."
        if "image" in pl:
            return "🖼️ Mock Image Insight: The image has balanced brightness."
        return "🤖 Mock General Insight: The system detected a general prompt."


# =======================================================================
# ⭐ DATA INSIGHT GENERATOR
# =======================================================================

class DataInsightGenerator(AIEngine):
    def analyze_dataset(self, data_summary: Dict) -> str:

        prompt = f"""
Analyze this dataset:

Rows: {data_summary.get('rows')}
Columns: {data_summary.get('columns')}
Numeric Columns: {data_summary.get('numeric_columns')}
Missing Values: {data_summary.get('missing_values')}

Provide:
1. Data quality assessment
2. Key observations
3. Patterns
4. Recommendations
"""
        return self.generate(prompt)


# =======================================================================
# ⭐ TEXT INSIGHT GENERATOR
# =======================================================================

class TextInsightGenerator(AIEngine):
    def enhance_summary(self, text: str, basic_summary: str) -> str:
        prompt = f"""
Improve this summary:

Original: {text}
Basic: {basic_summary}

Provide a better 2-line summary.
"""
        return self.generate(prompt)


# =======================================================================
# ⭐ IMAGE INSIGHT GENERATOR
# =======================================================================

class ImageInsightGenerator(AIEngine):
    def interpret_image_analysis(self, image_data: Dict) -> str:
        prompt = f"""
Interpret image analysis:

Brightness: {image_data.get('brightness')}
Edges: {image_data.get('edges')}
Color Variety: {image_data.get('color_variety')}

Give insights.
"""
        return self.generate(prompt)


# =======================================================================
# ⭐ MAIN TEST RUNNER (OUTPUT APPEARS HERE)
# =======================================================================

if __name__ == "__main__":

    print("\n" + "="*80)
    print("🧠 GEMINI AI ENGINE TEST")
    print("="*80)

    # TEST 1 – BASIC ENGINE
    engine = AIEngine(provider="gemini", api_key=Config.GEMINI_API_KEY)
    print("\n--- TEST 1: Basic Prompt ---")
    print(engine.generate("Give a short insight about data analysis."))

    # TEST 2 – DATA INSIGHTS
    print("\n--- TEST 2: Data Insight Generator ---")
    data_gen = DataInsightGenerator(provider="gemini", api_key=Config.GEMINI_API_KEY)
    print(data_gen.analyze_dataset({
        "rows": 1000,
        "columns": 8,
        "numeric_columns": ["sales", "profit"],
        "missing_values": 12
    }))

    # TEST 3 – TEXT INSIGHT
    print("\n--- TEST 3: Text Insight Generator ---")
    text_gen = TextInsightGenerator(provider="gemini", api_key=Config.GEMINI_API_KEY)
    print(text_gen.enhance_summary(
        "This product is amazing and works perfectly!",
        "Great product"
    ))

    # TEST 4 – IMAGE INSIGHT
    print("\n--- TEST 4: Image Insight Generator ---")
    img_gen = ImageInsightGenerator(provider="gemini", api_key=Config.GEMINI_API_KEY)
    print(img_gen.interpret_image_analysis({
        "brightness": 180,
        "edges": "medium",
        "color_variety": "high"
    }))

    print("\n\n✅ TEST COMPLETE")
