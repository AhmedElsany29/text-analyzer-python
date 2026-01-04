import os
import json
from openai import OpenAI

# Initialize the OpenAI client (pre-configured in the environment)
client = OpenAI()

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
        # Fallback to a basic implementation if LLM fails
        return {
            "word_count": len(text.split()),
            "sentence_count": text.count('.') + text.count('!') + text.count('?'),
            "top_words": [],
            "error": str(e)
        }

def main():
    try:
        with open('sample_text.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("Analyzing text using LLM... please wait.")
        stats = analyze_text_with_llm(content)
        
        print("\n--- Text Analysis Results (LLM-powered) ---")
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
