import cv2
import numpy as np
from PIL import Image
import os

# Tesseract configuration
try:
    import pytesseract
    # If Tesseract is not in PATH, specify the path here
    # Uncomment and modify the line below if needed:
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("⚠️ pytesseract not installed. OCR features will be disabled.")

class ImageAnalyzer:
    """
    Analyze images - extract text, metadata, and visual features
    """
    
    def __init__(self, image_path):
        """Initialize with image file path"""
        self.image_path = image_path
        self.image = None
        self.pil_image = None
        
    def load_image(self):
        """Load image using both OpenCV and PIL"""
        try:
            # Check if file exists
            if not os.path.exists(self.image_path):
                print(f"✗ File not found: {self.image_path}")
                return False
            
            # Load with OpenCV (for analysis)
            self.image = cv2.imread(self.image_path)
            if self.image is None:
                print("✗ Failed to load image with OpenCV")
                return False
            
            # Load with PIL (for metadata)
            self.pil_image = Image.open(self.image_path)
            print(f"✓ Image loaded successfully!")
            print(f"  Path: {self.image_path}")
            return True
        except Exception as e:
            print(f"✗ Error loading image: {e}")
            return False
    
    def get_metadata(self):
        """Extract image metadata"""
        if self.pil_image is None or self.image is None:
            print("❌ Please load image first!")
            return None
        
        print("\n" + "="*80)
        print("📋 IMAGE METADATA")
        print("="*80)
        
        metadata = {
            'filename': os.path.basename(self.image_path),
            'format': self.pil_image.format,
            'mode': self.pil_image.mode,
            'width': self.pil_image.width,
            'height': self.pil_image.height,
            'aspect_ratio': round(self.pil_image.width / self.pil_image.height, 2),
            'size_pixels': self.pil_image.width * self.pil_image.height,
            'channels': self.image.shape[2] if len(self.image.shape) == 3 else 1
        }
        
        # Display metadata
        for key, value in metadata.items():
            print(f"  {key}: {value}")
        
        return metadata
    
    def extract_text(self):
        """Extract text from image using OCR"""
        if self.image is None:
            print("❌ Please load image first!")
            return None
        
        if not TESSERACT_AVAILABLE:
            print("\n" + "="*80)
            print("📝 TEXT EXTRACTION (OCR)")
            print("="*80)
            print("❌ Tesseract OCR not available.")
            print("  Install: pip install pytesseract")
            print("  And download Tesseract from:")
            print("  https://github.com/UB-Mannheim/tesseract/wiki")
            return None
        
        print("\n" + "="*80)
        print("📝 TEXT EXTRACTION (OCR)")
        print("="*80)
        
        try:
            # Convert to RGB for Tesseract
            rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_image)
            
            # Extract text
            print("  Extracting text...", end=' ')
            text = pytesseract.image_to_string(pil_img)
            
            # Get detailed data with confidence scores
            data = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT)
            
            # Count words with confidence > 60
            confident_words = sum(1 for conf in data['conf'] if str(conf).isdigit() and int(conf) > 60)
            
            result = {
                'text': text.strip(),
                'word_count': len(text.split()),
                'character_count': len(text),
                'confident_words': confident_words,
                'has_text': len(text.strip()) > 0
            }
            
            print("✓")
            
            if result['has_text']:
                print(f"\n  Words found: {result['word_count']}")
                print(f"  Characters: {result['character_count']}")
                print(f"  High confidence words: {result['confident_words']}")
                print(f"\n  Extracted Text:")
                print("  " + "-"*76)
                preview = text[:500] + ("..." if len(text) > 500 else "")
                for line in preview.split('\n'):
                    if line.strip():
                        print(f"  {line}")
                print("  " + "-"*76)
            else:
                print("  No text detected in image")
            
            return result
            
        except Exception as e:
            print(f"✗ Error: {e}")
            if "tesseract is not installed" in str(e).lower():
                print("\n  💡 Tesseract not found! Please:")
                print("     1. Install from: https://github.com/UB-Mannheim/tesseract/wiki")
                print("     2. Add to PATH or set pytesseract.pytesseract.tesseract_cmd")
            return {
                'text': '',
                'error': str(e),
                'has_text': False
            }
    
    def analyze_colors(self):
        """Analyze dominant colors in the image"""
        if self.image is None:
            print("❌ Please load image first!")
            return None
        
        print("\n" + "="*80)
        print("🎨 COLOR ANALYSIS")
        print("="*80)
        
        # Convert to RGB
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        
        # Reshape to list of pixels
        pixels = rgb_image.reshape(-1, 3)
        
        # Calculate average color
        avg_color = np.mean(pixels, axis=0).astype(int)
        
        # Calculate color distribution
        unique_colors = len(np.unique(pixels, axis=0))
        
        # Determine if image is mostly bright or dark
        brightness = np.mean(pixels)
        
        result = {
            'average_color': {
                'r': int(avg_color[0]),
                'g': int(avg_color[1]),
                'b': int(avg_color[2])
            },
            'unique_colors': unique_colors,
            'brightness': round(brightness, 2),
            'is_bright': brightness > 127,
            'color_variety': 'high' if unique_colors > 10000 else 'medium' if unique_colors > 1000 else 'low'
        }
        
        # Display results
        print(f"  Average Color (RGB): ({result['average_color']['r']}, "
              f"{result['average_color']['g']}, {result['average_color']['b']})")
        print(f"  Unique Colors: {result['unique_colors']:,}")
        print(f"  Brightness: {result['brightness']:.1f} / 255")
        print(f"  Image is: {'Bright' if result['is_bright'] else 'Dark'}")
        print(f"  Color Variety: {result['color_variety']}")
        
        return result
    
    def detect_edges(self):
        """Detect edges in the image"""
        if self.image is None:
            print("❌ Please load image first!")
            return None
        
        print("\n" + "="*80)
        print("🔍 EDGE DETECTION")
        print("="*80)
        
        # Convert to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Apply Canny edge detection
        edges = cv2.Canny(gray, 100, 200)
        
        # Count edge pixels
        edge_pixels = np.sum(edges > 0)
        total_pixels = edges.size
        edge_percentage = (edge_pixels / total_pixels) * 100
        
        result = {
            'edge_pixels': int(edge_pixels),
            'total_pixels': int(total_pixels),
            'edge_percentage': round(edge_percentage, 2),
            'complexity': 'high' if edge_percentage > 20 else 'medium' if edge_percentage > 10 else 'low'
        }
        
        # Display results
        print(f"  Edge Pixels: {result['edge_pixels']:,} / {result['total_pixels']:,}")
        print(f"  Edge Percentage: {result['edge_percentage']:.2f}%")
        print(f"  Image Complexity: {result['complexity']}")
        
        return result
    
    def full_analysis(self):
        """Perform complete image analysis"""
        print("\n" + "="*80)
        print("🖼️  COMPLETE IMAGE ANALYSIS")
        print("="*80)
        
        if not self.load_image():
            return None
        
        results = {
            'metadata': self.get_metadata(),
            'text_extraction': self.extract_text(),
            'color_analysis': self.analyze_colors(),
            'edge_detection': self.detect_edges()
        }
        
        print("\n" + "="*80)
        print("✅ IMAGE ANALYSIS COMPLETE")
        print("="*80)
        
        return results


# ===========================================
# TEST CODE
# ===========================================

if __name__ == "__main__":
    print("="*80)
    print("🧠 SMART INSIGHT ENGINE - WEEK 2: IMAGE ANALYSIS TEST")
    print("="*80)
    
    # Check if test images exist
    test_images = [
        'data/test_image.png',
        'data/test_image.jpg',
        'uploads/sample.jpg'
    ]
    
    image_found = False
    for img_path in test_images:
        if os.path.exists(img_path):
            image_found = True
            print(f"\n✓ Found test image: {img_path}")
            
            # Analyze the image
            analyzer = ImageAnalyzer(img_path)
            results = analyzer.full_analysis()
            
            break
    
    if not image_found:
        print("\n⚠️ No test images found!")
        print("\n💡 To test image analysis:")
        print("  1. Run: python create_test_image.py")
        print("  2. Or place any image in 'data/' folder")
        print("  3. Then run this script again")
    
    print("\n" + "="*80)
    print("Week 2 - Image Module Complete! ✅")
    print("="*80)