import nltk

print("Downloading NLTK data...")
print("="*60)

# Download required packages
packages = [
    'punkt',           # Sentence tokenizer
    'stopwords',       # Common words to filter
    'averaged_perceptron_tagger',  # Part-of-speech tagger
    'brown',           # Brown corpus
    'wordnet'          # WordNet database
]

for package in packages:
    print(f"Downloading {package}...", end=' ')
    try:
        nltk.download(package, quiet=True)
        print("✓")
    except Exception as e:
        print(f"✗ Error: {e}")

print("="*60)
print("NLTK data download complete!")