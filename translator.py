#!/usr/bin/env python3
"""
Simple Text Translator using Google Translate API
Supports multiple languages and batch translation
"""

from googletrans import Translator
import sys
import json

class SimpleTranslator:
    def __init__(self):
        self.translator = Translator()
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh-cn': 'Chinese (Simplified)',
            'zh-tw': 'Chinese (Traditional)',
            'hi': 'Hindi',
            'ar': 'Arabic',
            'tr': 'Turkish',
        }

    def translate(self, text, src_lang='auto', dest_lang='en'):
        """Translate text from source language to destination language"""
        try:
            if not text or not text.strip():
                return {'success': False, 'error': 'Text cannot be empty'}
            
            result = self.translator.translate(text, src=src_lang, dest=dest_lang)
            return {
                'success': True,
                'original': text,
                'translated': result.text,
                'source_lang': src_lang,
                'dest_lang': dest_lang
            }
        except Exception as e:
            return {'success': False, 'error': f"Translation failed: {str(e)}"}

    def detect_language(self, text):
        """Detect the language of the given text"""
        try:
            if not text or not text.strip():
                return {'success': False, 'error': 'Text cannot be empty'}
            
            detection = self.translator.detect(text)
            lang_code = detection.lang
            lang_name = self.supported_languages.get(lang_code, 'Unknown')
            confidence = detection.confidence if detection.confidence else 0.0
            
            return {
                'success': True,
                'language': lang_name,
                'code': lang_code,
                'confidence': float(confidence) if confidence else 0.0
            }
        except Exception as e:
            return {'success': False, 'error': f"Detection failed: {str(e)}"}

    def list_languages(self):
        """List all supported languages"""
        return self.supported_languages

    def interactive_mode(self):
        """Run translator in interactive mode"""
        print("\n" + "="*60)
        print("          Welcome to Python Translator 🌍")
        print("="*60)
        
        print("\nSupported languages:")
        for code, name in self.supported_languages.items():
            print(f"  {code:10} : {name}")
        
        while True:
            print("\n" + "-"*60)
            print("Options:")
            print("  1. Translate text")
            print("  2. Detect language")
            print("  3. List languages")
            print("  4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                text = input("Enter text to translate: ").strip()
                if not text:
                    print("❌ Please enter some text")
                    continue
                
                src_lang = input("Source language (default: auto-detect): ").strip() or 'auto'
                dest_lang = input("Destination language (default: en): ").strip() or 'en'
                
                result = self.translate(text, src_lang, dest_lang)
                if result['success']:
                    print(f"\n✅ Translation:")
                    print(f"   Original: {result['original']}")
                    print(f"   Translated: {result['translated']}")
                else:
                    print(f"\n❌ {result['error']}")
                
            elif choice == '2':
                text = input("Enter text to detect: ").strip()
                if not text:
                    print("❌ Please enter some text")
                    continue
                
                detection = self.detect_language(text)
                if detection['success']:
                    confidence_str = f"{detection['confidence']*100:.2f}%" if detection['confidence'] else "Unknown"
                    print(f"\n✅ Detected Language: {detection['language']} ({detection['code']})")
                    print(f"   Confidence: {confidence_str}")
                else:
                    print(f"\n❌ {detection['error']}")
                    
            elif choice == '3':
                print("\nSupported languages:")
                for code, name in self.list_languages().items():
                    print(f"  {code:10} : {name}")
                    
            elif choice == '4':
                print("\n👋 Thank you for using Python Translator!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-4")


def main():
    translator = SimpleTranslator()
    
    # If command line arguments are provided, use them
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h']:
            print("Usage: python translator.py [text] [source_lang] [dest_lang]")
            print("\nExamples:")
            print("  python translator.py 'Hello' en es")
            print("  python translator.py 'Bonjour' fr en")
            print("  python translator.py 'こんにちは'")
            sys.exit(0)
        
        text = sys.argv[1]
        src_lang = sys.argv[2] if len(sys.argv) > 2 else 'auto'
        dest_lang = sys.argv[3] if len(sys.argv) > 3 else 'en'
        
        result = translator.translate(text, src_lang, dest_lang)
        if result['success']:
            print(f"Original: {result['original']}")
            print(f"Translated: {result['translated']}")
        else:
            print(f"Error: {result['error']}")
    else:
        # Run interactive mode
        translator.interactive_mode()


if __name__ == "__main__":
    main()
