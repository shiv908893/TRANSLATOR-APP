#!/usr/bin/env python3
"""
Installation Verification Script
Run this to verify the translator is properly installed
"""

import sys
import subprocess
import importlib

def check_python_version():
    """Check Python version"""
    print("\n" + "="*60)
    print("Checking Python Version")
    print("="*60)
    
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("✅ Python version is compatible (3.7+)")
        return True
    else:
        print("❌ Python 3.7+ required")
        return False

def check_dependencies():
    """Check required dependencies"""
    print("\n" + "="*60)
    print("Checking Dependencies")
    print("="*60)
    
    dependencies = {
        'googletrans': 'Google Translate API',
        'flask': 'Flask Web Framework',
        'requests': 'HTTP Library for Testing',
    }
    
    all_installed = True
    
    for module_name, description in dependencies.items():
        try:
            importlib.import_module(module_name)
            print(f"✅ {description} ({module_name})")
        except ImportError:
            print(f"❌ {description} ({module_name}) - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_files():
    """Check if all required files exist"""
    print("\n" + "="*60)
    print("Checking Project Files")
    print("="*60)
    
    import os
    
    required_files = {
        'translator.py': 'Core translator module',
        'app.py': 'Flask web application',
        'test_api.py': 'API test suite',
        'examples.py': 'Code examples',
        'requirements.txt': 'Dependencies file',
        'templates/index.html': 'Web interface',
        'README.md': 'Documentation',
        'QUICKSTART.md': 'Quick start guide',
    }
    
    all_exist = True
    
    for file_path, description in required_files.items():
        if os.path.exists(file_path):
            print(f"✅ {description} ({file_path})")
        else:
            print(f"❌ {description} ({file_path}) - NOT FOUND")
            all_exist = False
    
    return all_exist

def test_translator_import():
    """Test if translator can be imported"""
    print("\n" + "="*60)
    print("Testing Translator Import")
    print("="*60)
    
    try:
        from translator import SimpleTranslator
        print("✅ Translator module imports successfully")
        
        # Create instance
        t = SimpleTranslator()
        print("✅ SimpleTranslator class instantiates successfully")
        
        # Check methods
        methods = ['translate', 'detect_language', 'list_languages']
        for method in methods:
            if hasattr(t, method):
                print(f"✅ Method '{method}' exists")
            else:
                print(f"❌ Method '{method}' not found")
        
        return True
    except Exception as e:
        print(f"❌ Error importing translator: {e}")
        return False

def test_translation():
    """Test basic translation"""
    print("\n" + "="*60)
    print("Testing Translation Functionality")
    print("="*60)
    
    try:
        from translator import SimpleTranslator
        t = SimpleTranslator()
        
        # Test translation
        result = t.translate("Hello", src_lang="en", dest_lang="es")
        
        if result['success']:
            print(f"✅ Translation works: '{result['original']}' -> '{result['translated']}'")
        else:
            print(f"❌ Translation failed: {result['error']}")
            return False
        
        # Test detection
        detection = t.detect_language("Bonjour")
        
        if detection['success']:
            print(f"✅ Detection works: Detected '{detection['language']}'")
        else:
            print(f"❌ Detection failed: {detection['error']}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error during translation test: {e}")
        return False

def check_flask_app():
    """Check if Flask app is importable"""
    print("\n" + "="*60)
    print("Testing Flask Application")
    print("="*60)
    
    try:
        import app
        print("✅ Flask app imports successfully")
        
        # Check if required attributes exist
        if hasattr(app, 'app'):
            print("✅ Flask app instance exists")
        else:
            print("❌ Flask app instance not found")
            return False
        
        # Check routes
        routes = ['/api/translate', '/api/detect', '/api/languages', '/api/health', '/']
        print("✅ API routes configured:")
        for route in routes:
            print(f"   - {route}")
        
        return True
    except Exception as e:
        print(f"❌ Error loading Flask app: {e}")
        return False

def main():
    """Run all checks"""
    print("\n" + "#"*60)
    print("# Python Translator - Installation Verification")
    print("#"*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Files", check_files),
        ("Translator Import", test_translator_import),
        ("Translation Test", test_translation),
        ("Flask Application", check_flask_app),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n❌ Error during {check_name}: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    for check_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{check_name:30} {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL CHECKS PASSED - Translator is ready to use!")
        print("\nNext steps:")
        print("  1. Run CLI:        python translator.py")
        print("  2. Run Web UI:     python app.py")
        print("  3. Run Tests:      python test_api.py")
        print("  4. See Examples:   python examples.py")
    else:
        print("❌ Some checks failed - Please fix errors above")
        print("\nTo install missing dependencies:")
        print("  pip install -r requirements.txt")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
