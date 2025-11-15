
from PIL import Image, ImageDraw, ImageFont
import os

# Create data folder if it doesn't exist
os.makedirs('data', exist_ok=True)

# Create a simple image with text
img = Image.new('RGB', (800, 400), color='white')
draw = ImageDraw.Draw(img)

# Add text
text = """
Smart Insight Engine

This is a test image with text.
OCR should be able to read this!
"""

# Try to use a default font
try:
    font = ImageFont.truetype("arial.ttf", 36)
except:
    font = ImageFont.load_default()

draw.text((50, 50), text, fill='black', font=font)

# Add some colored shapes
draw.rectangle([50, 300, 200, 350], fill='red')
draw.rectangle([250, 300, 400, 350], fill='green')
draw.rectangle([450, 300, 600, 350], fill='blue')

# Save
img.save('data/test_image.png')
print("✓ Test image created: data/test_image.png")