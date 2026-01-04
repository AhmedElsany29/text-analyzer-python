import os
import json
import httpx
from openai import OpenAI

def get_openai_client():
    """
    Initializes the OpenAI client with a fix for the 'proxies' keyword argument error.
    This error often occurs due to version mismatches between openai and httpx.
    """
    try:
        # We explicitly create an httpx client without the problematic proxies argument
        # if it's causing issues, or just use the default if it works.
        # In many environments, simply ensuring httpx is used correctly fixes it.
        http_client = httpx.Client()
        return OpenAI(http_client=http_client)
    except TypeError:
        # Fallback for older versions or specific environment configurations
        return OpenAI()
    except Exception as e:
        print(f"Warning: Could not initialize OpenAI client: {e}")
        return None

def analyze_text_with_llm(text):
    """
    Analyzes the input text using an LLM and returns statistics.
    """
    if not text:
        return {
            "word_count": 0,
            "sentence_count": 0,
            "top_words": []
        }

    client = get_openai_client()
    
    if not client:
        return fallback_analysis(text)

    prompt = f"""
    Analyze the following text and provide statistics in JSON format.
    Requirements:
    1. Word count (total number of words).
    2. Sentence count (total number of sentences).
    3. Top 10 most frequent words, ignoring punctuation and case.

    Text:
    \"\"\"{text}\"\"\"

    Return ONLY a JSON object with the following keys:
    "word_count": int,
    "sentence_count": int,
    "top_words": [[word, frequency], ...]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes text and returns structured JSON data."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return fallback_analysis(text)

def fallback_analysis(text):
    """
    Basic text analysis implementation as a fallback.
    """
    import re
    from collections import Counter
    import string

    # Sentence count
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]
    
    # Word count and frequency
    translator = str.maketrans('', '', string.punctuation.replace("'", "").replace("-", ""))
    clean_text = text.translate(translator).lower()
    words = [w.strip("'-") for w in clean_text.split() if w.strip("'-")]
    
    word_freq = Counter(words)
    
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "top_words": word_freq.most_common(10),
        "note": "Analysis performed using fallback method due to LLM error."
    }

def main():
    try:
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            print("Warning: OPENAI_API_KEY environment variable not set.")
            print("The script will attempt to use the fallback analysis method.")

        with open('sample_text.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("Analyzing text... please wait.")
        stats = analyze_text_with_llm(content)
        
        print("\n--- Text Analysis Results ---")
        if "note" in stats:
            print(f"Note: {stats['note']}")
            
        print(f"Word Count: {stats.get('word_count')}")
        print(f"Sentence Count: {stats.get('sentence_count')}")
        print("\nTop 10 Most Frequent Words:")
        for item in stats.get('top_words', []):
            if isinstance(item, list) and len(item) == 2:
                word, freq = item
                print(f"{word}: {freq}")
            
    except FileNotFoundError:
        print("Error: sample_text.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
