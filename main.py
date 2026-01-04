import re
from collections import Counter
import string

def analyze_text(text):
    """
    Analyzes the input text and returns statistics.
    """
    if not text:
        return {
            "word_count": 0,
            "sentence_count": 0,
            "top_words": []
        }

    # 1. Sentence count
    # Sentences usually end with ., !, or ?
    # We use regex to find sentence endings, handling potential multiple punctuation like "..."
    sentences = re.split(r'[.!?]+', text)
    # Filter out empty strings from the split
    sentences = [s for s in sentences if s.strip()]
    sentence_count = len(sentences)

    # 2. Word count and Top 10 words
    # Remove punctuation for word counting and frequency analysis
    # We'll keep hyphens and apostrophes as they are often part of words (e.g., "don't", "end-to-end")
    # But for "ignoring punctuation" requirement, we'll be careful.
    
    # First, let's normalize the text: lowercase and replace punctuation with spaces
    # We'll use a regex that keeps alphanumeric characters and some internal word symbols
    # but treats most punctuation as delimiters.
    
    # Create a translation table to remove punctuation
    translator = str.maketrans('', '', string.punctuation.replace("'", "").replace("-", ""))
    clean_text = text.translate(translator).lower()
    
    # Split into words
    words = clean_text.split()
    word_count = len(words)

    # 3. Top 10 most frequent words
    # We might want to strip leading/trailing hyphens/apostrophes from words
    cleaned_words = [w.strip("'-") for w in words]
    cleaned_words = [w for w in cleaned_words if w] # Remove empty strings
    
    word_freq = Counter(cleaned_words)
    top_10_words = word_freq.most_common(10)

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "top_words": top_10_words
    }

def main():
    try:
        with open('sample_text.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        stats = analyze_text(content)
        
        print("--- Text Analysis Results ---")
        print(f"Word Count: {stats['word_count']}")
        print(f"Sentence Count: {stats['sentence_count']}")
        print("\nTop 10 Most Frequent Words:")
        for word, freq in stats['top_words']:
            print(f"{word}: {freq}")
            
    except FileNotFoundError:
        print("Error: sample_text.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
