#!/usr/bin/env python3
"""
API Test Suite for Python Translator
Test the REST API endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("Testing: Health Check")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_languages():
    """Test languages endpoint"""
    print("\n" + "="*60)
    print("Testing: Get Languages")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/api/languages")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Supported languages: {data['total']}")
        print(f"Languages: {json.dumps(data['languages'], indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_translate():
    """Test translate endpoint"""
    print("\n" + "="*60)
    print("Testing: Translation API")
    print("="*60)
    test_cases = [
        {"text": "Hello", "source_lang": "en", "dest_lang": "es"},
        {"text": "Bonjour", "source_lang": "fr", "dest_lang": "en"},
        {"text": "こんにちは", "source_lang": "ja", "dest_lang": "en"},
    ]
    
    all_passed = True
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"  Text: {test_case['text']}")
        print(f"  From: {test_case['source_lang']} -> To: {test_case['dest_lang']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/translate",
                json=test_case,
                headers={"Content-Type": "application/json"}
            )
            print(f"  Status: {response.status_code}")
            data = response.json()
            
            if data.get('success'):
                print(f"  ✅ Original: {data['original']}")
                print(f"  ✅ Translated: {data['translated']}")
            else:
                print(f"  ❌ Error: {data.get('error')}")
                all_passed = False
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            all_passed = False
    
    return all_passed

def test_detect():
    """Test detect endpoint"""
    print("\n" + "="*60)
    print("Testing: Language Detection API")
    print("="*60)
    test_cases = [
        "Hello, how are you?",
        "Bonjour, comment allez-vous?",
        "Hola, ¿cómo estás?",
        "こんにちは、お元気ですか？",
    ]
    
    all_passed = True
    for i, text in enumerate(test_cases, 1):
        print(f"\nTest {i}: {text}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/detect",
                json={"text": text},
                headers={"Content-Type": "application/json"}
            )
            print(f"  Status: {response.status_code}")
            data = response.json()
            
            if data.get('success'):
                print(f"  ✅ Detected: {data['language']} ({data['code']})")
                if data['confidence']:
                    print(f"  ✅ Confidence: {data['confidence']*100:.2f}%")
            else:
                print(f"  ❌ Error: {data.get('error')}")
                all_passed = False
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            all_passed = False
    
    return all_passed

def test_error_handling():
    """Test error handling"""
    print("\n" + "="*60)
    print("Testing: Error Handling")
    print("="*60)
    
    all_passed = True
    
    # Test empty text
    print("\nTest 1: Empty text")
    try:
        response = requests.post(
            f"{BASE_URL}/api/translate",
            json={"text": "", "source_lang": "en", "dest_lang": "es"},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 400:
            print(f"  ✅ Correctly returned 400: {response.json()['error']}")
        else:
            print(f"  ❌ Expected 400, got {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        all_passed = False
    
    # Test invalid endpoint
    print("\nTest 2: Invalid endpoint")
    try:
        response = requests.get(f"{BASE_URL}/api/invalid")
        if response.status_code == 404:
            print(f"  ✅ Correctly returned 404")
        else:
            print(f"  ❌ Expected 404, got {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        all_passed = False
    
    return all_passed

def run_all_tests():
    """Run all tests"""
    print("\n" + "#"*60)
    print("# Python Translator API Test Suite")
    print("#"*60)
    
    results = []
    
    results.append(("Health Check", test_health()))
    results.append(("Get Languages", test_languages()))
    results.append(("Translation", test_translate()))
    results.append(("Detection", test_detect()))
    results.append(("Error Handling", test_error_handling()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:30} {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    print("="*60 + "\n")

if __name__ == "__main__":
    print("Make sure the Flask server is running!")
    print("Run: python app.py")
    
    input("\nPress Enter to start tests...")
    time.sleep(1)
    
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to Flask server")
        print("Make sure Flask is running on http://localhost:5000")
