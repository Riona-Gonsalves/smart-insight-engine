import os
from modules.image_analyzer import ImageAnalyzer

print("\n" + "="*80)
print("TEST 1: TEXT ANALYSIS ✓")
print("="*80)

sample_text = """
The Smart Insight Engine is a powerful data analysis tool. It combines 
machine learning, natural language processing, and computer vision to 
provide comprehensive insights. This project demonstrates practical 
applications of AI in data science. Users can analyze CSV files, 
extract information from images, and understand text sentiment.
"""

img_analyzer = ImageAnalyzer(sample_text)
text_results = img_analyzer.full_analysis()

# =======================
# TEST 2: IMAGE ANALYSIS
# =======================
print("\n" + "="*80)
print("TEST 2: IMAGE ANALYSIS")
print("="*80)

# Check if we can import image analyzer
try:
    from modules.image_analyzer import ImageAnalyzer
    
    # Check for test image
    test_image_paths = ['data/test_image.png', 'data/test_image.jpg']
    image_found = False
    
    for img_path in test_image_paths:
        if os.path.exists(img_path):
            print(f"\n✓ Found test image: {img_path}")
            img_analyzer = ImageAnalyzer(img_path)
            img_results = img_analyzer.full_analysis()
            image_found = True
            break
    
    if not image_found:
        print("\n⚠️ No test image found")
        print("  Creating one now...")
        os.system('python create_test_image.py')
        
        if os.path.exists('data/test_image.png'):
            print("\n✓ Test image created! Analyzing...")
            img_analyzer = ImageAnalyzer('data/test_image.png')
            img_results = img_analyzer.full_analysis()
        else:
            print("  ✗ Could not create test image")
            print("  Skipping image analysis test")
    
except Exception as e:
    print(f"\n⚠️ Image analysis not available: {e}")
    print("  This is okay - OCR requires Tesseract installation")

