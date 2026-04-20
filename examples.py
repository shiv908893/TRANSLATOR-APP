#!/usr/bin/env python3
"""
Python Translator - Code Examples
Demonstrates various ways to use the translator
"""

from translator import SimpleTranslator
import json

def example_1_basic_translation():
    """Example 1: Basic translation"""
    print("\n" + "="*60)
    print("Example 1: Basic Translation")
    print("="*60)
    
    translator = SimpleTranslator()
    
    # Translate English to Spanish
    result = translator.translate("Hello, how are you?", src_lang="en", dest_lang="es")
    
    if result['success']:
        print(f"Original: {result['original']}")
        print(f"Translated: {result['translated']}")
    else:
        print(f"Error: {result['error']}")


def example_2_auto_detect():
    """Example 2: Auto-detect language"""
    print("\n" + "="*60)
    print("Example 2: Auto-Detect Language")
    print("="*60)
    
    translator = SimpleTranslator()
    
    # Translate with auto-detection
    result = translator.translate("Bonjour mon ami", dest_lang="en")
    
    if result['success']:
        print(f"Original: {result['original']}")
        print(f"Detected from: {result['source_lang']}")
        print(f"Translated to: {result['translated']}")
    else:
        print(f"Error: {result['error']}")


def example_3_language_detection():
    """Example 3: Detect language of text"""
    print("\n" + "="*60)
    print("Example 3: Language Detection")
    print("="*60)
    
    translator = SimpleTranslator()
    
    test_texts = [
        "Hello, this is English",
        "Bonjour, ceci est français",
        "Hola, esto es español",
        "こんにちは、これは日本語です",
    ]
    
    for text in test_texts:
        result = translator.detect_language(text)
        if result['success']:
            confidence = f"{result['confidence']*100:.1f}%" if result['confidence'] else "N/A"
            print(f"\n'{text[:30]}...'")
            print(f"  Detected: {result['language']} ({result['code']})")
            print(f"  Confidence: {confidence}")
        else:
            print(f"Error: {result['error']}")


def example_4_batch_translation():
    """Example 4: Translate multiple texts"""
    print("\n" + "="*60)
    print("Example 4: Batch Translation")
    print("="*60)
    
    translator = SimpleTranslator()
    
    texts = [
        "Good morning",
        "Good afternoon", 
        "Good evening",
        "Good night"
    ]
    
    print("Translating English greetings to Spanish:\n")
    
    translations = []
    for text in texts:
        result = translator.translate(text, src_lang="en", dest_lang="es")
        if result['success']:
            translations.append({
                'english': text,
                'spanish': result['translated']
            })
            print(f"{text:20} -> {result['translated']}")
    
    return translations


def example_5_json_output():
    """Example 5: Working with JSON responses"""
    print("\n" + "="*60)
    print("Example 5: JSON Response Handling")
    print("="*60)
    
    translator = SimpleTranslator()
    
    result = translator.translate("Python is awesome", src_lang="en", dest_lang="fr")
    
    # Pretty print JSON response
    print("\nFull Response:")
    print(json.dumps(result, indent=2))
    
    # Access specific fields
    print(f"\nAccessing specific fields:")
    print(f"Original text: {result['original']}")
    print(f"Translated text: {result['translated']}")
    print(f"Source language: {result['source_lang']}")
    print(f"Destination language: {result['dest_lang']}")


def example_6_error_handling():
    """Example 6: Error handling"""
    print("\n" + "="*60)
    print("Example 6: Error Handling")
    print("="*60)
    
    translator = SimpleTranslator()
    
    # Example 1: Empty text
    print("\nTest 1: Empty text")
    result = translator.translate("", src_lang="en", dest_lang="es")
    print(f"Success: {result['success']}")
    print(f"Error: {result['error']}")
    
    # Example 2: Successful translation
    print("\nTest 2: Valid translation")
    result = translator.translate("Hello", src_lang="en", dest_lang="es")
    print(f"Success: {result['success']}")
    print(f"Translation: {result['translated']}")


def example_7_supported_languages():
    """Example 7: List supported languages"""
    print("\n" + "="*60)
    print("Example 7: Supported Languages")
    print("="*60)
    
    translator = SimpleTranslator()
    languages = translator.list_languages()
    
    print(f"\nTotal supported languages: {len(languages)}\n")
    
    # Print in columns
    items = list(languages.items())
    for i in range(0, len(items), 3):
        row = items[i:i+3]
        for code, name in row:
            print(f"{code:10} - {name:20}", end="  ")
        print()


def example_8_multi_language_chain():
    """Example 8: Translate through multiple languages"""
    print("\n" + "="*60)
    print("Example 8: Multi-Language Chain Translation")
    print("="*60)
    
    translator = SimpleTranslator()
    
    original_text = "Programming is fun"
    current_text = original_text
    current_lang = "en"
    
    languages_chain = ["en", "es", "fr", "de", "en"]
    print(f"\nTranslating through: {' -> '.join(languages_chain)}\n")
    
    for next_lang in languages_chain[1:]:
        result = translator.translate(current_text, src_lang=current_lang, dest_lang=next_lang)
        if result['success']:
            current_text = result['translated']
            print(f"{current_lang} ({current_text})")
            current_lang = next_lang
        else:
            print(f"Error: {result['error']}")
            break


def example_9_language_specific_translations():
    """Example 9: Translate to multiple languages"""
    print("\n" + "="*60)
    print("Example 9: Translate to Multiple Languages")
    print("="*60)
    
    translator = SimpleTranslator()
    
    text = "Welcome to Python Translator"
    target_languages = ["es", "fr", "de", "ja", "zh-cn"]
    
    print(f"\nOriginal: {text}\n")
    
    for lang_code in target_languages:
        lang_name = translator.list_languages()[lang_code]
        result = translator.translate(text, src_lang="en", dest_lang=lang_code)
        
        if result['success']:
            print(f"{lang_name:20} : {result['translated']}")


def example_10_confidence_filtering():
    """Example 10: Filter detections by confidence"""
    print("\n" + "="*60)
    print("Example 10: Confidence-Based Filtering")
    print("="*60)
    
    translator = SimpleTranslator()
    
    test_texts = [
        "Hello world",
        "Hi",
        "This is a longer English text that should have higher confidence",
    ]
    
    print("\nDetections with confidence threshold:\n")
    
    for text in test_texts:
        result = translator.detect_language(text)
        if result['success']:
            confidence = result.get('confidence', 0)
            confidence_pct = f"{confidence*100:.1f}%" if confidence else "N/A"
            
            status = "✅ HIGH" if confidence and confidence > 0.5 else "⚠️  LOW"
            
            print(f"Text: '{text}'")
            print(f"  Detected: {result['language']} | Confidence: {confidence_pct} {status}\n")


def main():
    """Run all examples"""
    print("\n" + "#"*60)
    print("# Python Translator - Code Examples")
    print("#"*60)
    
    examples = [
        example_1_basic_translation,
        example_2_auto_detect,
        example_3_language_detection,
        example_4_batch_translation,
        example_5_json_output,
        example_6_error_handling,
        example_7_supported_languages,
        example_8_multi_language_chain,
        example_9_language_specific_translations,
        example_10_confidence_filtering,
    ]
    
    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n❌ Error in {example_func.__name__}: {e}")
    
    print("\n" + "#"*60)
    print("# Examples Complete!")
    print("#"*60 + "\n")


if __name__ == "__main__":
    main()
