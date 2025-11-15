import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from textblob import TextBlob
from collections import Counter
import numpy as np

class TextAnalyzer:
    """
    Analyze text - sentiment, keywords, summary, readability
    """
    
    def __init__(self, text):
        """Initialize with text content"""
        self.text = text
        self.blob = TextBlob(text)
        self.sentences = sent_tokenize(text)
        self.words = word_tokenize(text.lower())
    
    def get_basic_stats(self):
        """Get basic text statistics"""
        print("\n" + "="*80)
        print("📊 BASIC TEXT STATISTICS")
        print("="*80)
        
        stats = {
            'character_count': len(self.text),
            'word_count': len(self.words),
            'sentence_count': len(self.sentences),
            'avg_word_length': round(np.mean([len(word) for word in self.words]), 2),
            'avg_sentence_length': round(len(self.words) / len(self.sentences), 2) if self.sentences else 0,
            'unique_words': len(set(self.words))
        }
        
        # Display stats
        print(f"  Characters: {stats['character_count']:,}")
        print(f"  Words: {stats['word_count']:,}")
        print(f"  Sentences: {stats['sentence_count']}")
        print(f"  Unique Words: {stats['unique_words']:,}")
        print(f"  Avg Word Length: {stats['avg_word_length']:.1f} characters")
        print(f"  Avg Sentence Length: {stats['avg_sentence_length']:.1f} words")
        
        return stats
    
    def sentiment_analysis(self):
        """Analyze sentiment of the text"""
        print("\n" + "="*80)
        print("😊 SENTIMENT ANALYSIS")
        print("="*80)
        
        sentiment = self.blob.sentiment
        
        # Classify sentiment
        if sentiment.polarity > 0.1:
            classification = 'positive'
            emoji = '😊'
        elif sentiment.polarity < -0.1:
            classification = 'negative'
            emoji = '😞'
        else:
            classification = 'neutral'
            emoji = '😐'
        
        result = {
            'polarity': round(sentiment.polarity, 3),  # -1 to 1
            'subjectivity': round(sentiment.subjectivity, 3),  # 0 to 1
            'classification': classification,
            'confidence': abs(sentiment.polarity)
        }
        
        # Display results
        print(f"  {emoji} Sentiment: {classification.upper()}")
        print(f"  Polarity: {result['polarity']:.3f} (range: -1 to 1)")
        print(f"    -1 = Very Negative, 0 = Neutral, 1 = Very Positive")
        print(f"  Subjectivity: {result['subjectivity']:.3f} (range: 0 to 1)")
        print(f"    0 = Objective, 1 = Subjective")
        print(f"  Confidence: {result['confidence']:.3f}")
        
        return result
    
    def extract_keywords(self, top_n=10):
        """Extract most common keywords (excluding stop words)"""
        print("\n" + "="*80)
        print(f"🔑 TOP {top_n} KEYWORDS")
        print("="*80)
        
        try:
            stop_words = set(stopwords.words('english'))
        except:
            print("  Downloading stopwords...")
            nltk.download('stopwords', quiet=True)
            stop_words = set(stopwords.words('english'))
        
        # Filter out stop words and punctuation
        filtered_words = [
            word for word in self.words 
            if word.isalnum() and word not in stop_words and len(word) > 3
        ]
        
        # Count frequency
        word_freq = Counter(filtered_words)
        keywords = word_freq.most_common(top_n)
        
        # Display keywords
        print("\n  Rank | Keyword        | Frequency")
        print("  " + "-"*40)
        for i, (word, freq) in enumerate(keywords, 1):
            print(f"  {i:2d}   | {word:14s} | {freq:3d}")
        
        return [{'word': word, 'frequency': freq} for word, freq in keywords]
    
    def extractive_summary(self, num_sentences=3):
        """Create extractive summary (most important sentences)"""
        print("\n" + "="*80)
        print(f"📝 EXTRACTIVE SUMMARY (Top {num_sentences} sentences)")
        print("="*80)
        
        if len(self.sentences) <= num_sentences:
            summary = ' '.join(self.sentences)
            print("\n  (Text is short, showing all sentences)")
        else:
            # Score sentences based on word frequency
            word_freq = Counter(self.words)
            
            sentence_scores = {}
            for i, sentence in enumerate(self.sentences):
                words = word_tokenize(sentence.lower())
                score = sum(word_freq.get(word, 0) for word in words)
                sentence_scores[i] = score / len(words) if words else 0
            
            # Get top sentences
            top_sentences = sorted(sentence_scores.items(), 
                                 key=lambda x: x[1], reverse=True)[:num_sentences]
            top_sentences = sorted(top_sentences, key=lambda x: x[0])  # Maintain order
            
            summary = ' '.join([self.sentences[i] for i, _ in top_sentences])
        
        # Display summary
        print("\n  " + "-"*76)
        print(f"  {summary}")
        print("  " + "-"*76)
        
        return summary
    
    def readability_score(self):
        """Calculate readability metrics"""
        print("\n" + "="*80)
        print("📚 READABILITY ANALYSIS")
        print("="*80)
        
        words = len(self.words)
        sentences = len(self.sentences)
        syllables = sum(self._count_syllables(word) for word in self.words)
        
        if sentences == 0 or words == 0:
            print("  ⚠️ Text too short for readability analysis")
            return None
        
        # Flesch Reading Ease Score
        flesch_score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        
        # Flesch-Kincaid Grade Level
        grade_level = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
        grade_level = round(max(0, grade_level), 1)
        
        # Classify difficulty
        if flesch_score >= 90:
            difficulty = 'very easy (5th grade)'
        elif flesch_score >= 80:
            difficulty = 'easy (6th grade)'
        elif flesch_score >= 70:
            difficulty = 'fairly easy (7th grade)'
        elif flesch_score >= 60:
            difficulty = 'standard (8th-9th grade)'
        elif flesch_score >= 50:
            difficulty = 'fairly difficult (10th-12th grade)'
        elif flesch_score >= 30:
            difficulty = 'difficult (college)'
        else:
            difficulty = 'very difficult (college graduate)'
        
        result = {
            'flesch_score': round(flesch_score, 2),
            'difficulty': difficulty,
            'grade_level': grade_level
        }
        
        # Display results
        print(f"  Flesch Reading Ease: {result['flesch_score']:.1f}")
        print(f"  Difficulty Level: {difficulty}")
        print(f"  Grade Level: {grade_level}")
        print(f"\n  💡 Interpretation:")
        print(f"     Higher Flesch score = Easier to read")
        print(f"     Grade level = Years of education needed")
        
        return result
    
    def _count_syllables(self, word):
        """Count syllables in a word (approximation)"""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Adjust for silent 'e'
        if word.endswith('e'):
            syllable_count -= 1
        
        return max(1, syllable_count)
    
    def full_analysis(self):
        """Perform complete text analysis"""
        print("\n" + "="*80)
        print("📄 COMPLETE TEXT ANALYSIS")
        print("="*80)
        
        results = {
            'basic_stats': self.get_basic_stats(),
            'sentiment': self.sentiment_analysis(),
            'keywords': self.extract_keywords(),
            'summary': self.extractive_summary(),
            'readability': self.readability_score()
        }
        
        print("\n" + "="*80)
        print("✅ TEXT ANALYSIS COMPLETE")
        print("="*80)
        
        return results


# ===========================================
# TEST CODE
# ===========================================

if __name__ == "__main__":
    print("="*80)
    print("🧠 SMART INSIGHT ENGINE - WEEK 2: TEXT ANALYSIS TEST")
    print("="*80)
    
    # Sample text for testing
    sample_text = """
    Artificial intelligence is transforming the world in unprecedented ways. 
    Machine learning algorithms are becoming more sophisticated, enabling 
    computers to learn from data and make intelligent decisions. Natural 
    language processing allows machines to understand and generate human 
    language with remarkable accuracy. The future of AI holds immense 
    potential for solving complex problems across various industries.
    
    Deep learning, a subset of machine learning, has revolutionized computer 
    vision and speech recognition. Neural networks with multiple layers can 
    now identify patterns and features that were previously impossible to 
    detect. This breakthrough has led to amazing applications in healthcare, 
    autonomous vehicles, and personalized recommendations.
    
    However, with great power comes great responsibility. Ethical considerations 
    around AI bias, privacy, and job displacement must be carefully addressed. 
    As we continue to advance these technologies, it's crucial to ensure they 
    benefit humanity as a whole and don't exacerbate existing inequalities.
    """
    
    print("\n📝 Analyzing sample text about Artificial Intelligence...")
    print("="*80)
    
    # Create analyzer
    analyzer = TextAnalyzer(sample_text)
    
    # Perform full analysis
    results = analyzer.full_analysis()
    
    print("\n" + "="*80)
    print("💡 TRY IT YOURSELF!")
    print("="*80)
    print("\n  Create a file 'test_text.py' with:")
    print("""
    from modules.text_analyzer import TextAnalyzer
    
    my_text = "Your text here..."
    analyzer = TextAnalyzer(my_text)
    analyzer.full_analysis()
    """)
    
    print("\n" + "="*80)
    print("Week 2 - Text Module Complete! ✅")
    print("Next: Combine Image + Text Analysis")
    print("="*80)