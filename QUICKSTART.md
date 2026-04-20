# 🚀 Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies (30 seconds)
```bash
pip install -r requirements.txt
```

### 2. Choose Your Interface

#### A. GUI - Best for Desktop Users ⭐ (RECOMMENDED)
```bash
python gui.py
```

**Features:**
- 🖥️ Professional desktop application
- 📝 Input/Output text windows
- 📜 Translation history panel
- 🔄 Swap languages with one click
- 📋 Copy/paste functionality
- 💾 Auto-save history
- ⌨️ Keyboard shortcuts (Ctrl+Enter, Ctrl+D, Ctrl+C)

---

#### B. CLI - Quickest Way to Translate
```bash
# Interactive mode
python translator.py

# Direct translation
python translator.py "Hello" en es
```

#### C. Web UI - Beautiful Interface
```bash
python app.py
```
Visit: http://localhost:5000

#### D. API - For Developers
```bash
python app.py  # Start server
```

Then test with:
```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "source_lang": "en", "dest_lang": "es"}'
```

---

## GUI Quick Start

**1. Launch GUI:**
```bash
python gui.py
```

**2. Basic Usage:**
- Select source and destination languages
- Enter text in the input window
- Click "TRANSLATE" or press Ctrl+Enter
- View result in output window
- History automatically saved

**3. Advanced Features:**
- **Detect Language:** Click to auto-detect input language
- **Swap Languages:** Click "⇄ Swap" to reverse translation
- **Copy Output:** Click to copy translation to clipboard
- **Export History:** Save all translations as JSON file

### Translation
```bash
# English to Spanish
python translator.py "Good morning" en es

# French to English  
python translator.py "Bonjour" fr en

# Auto-detect source language
python translator.py "こんにちは"
```

### Using in Python Code
```python
from translator import SimpleTranslator

t = SimpleTranslator()

# Translate
result = t.translate("Hello", src_lang="en", dest_lang="es")
print(result['translated'])  # Output: Hola

# Detect language
detected = t.detect_language("Bonjour")
print(detected['language'])  # Output: French
```

### API Testing
```bash
python test_api.py
```

---

## Supported Languages (14)

```
en - English        |  ja - Japanese      |  zh-cn - Chinese (Simplified)
es - Spanish        |  ko - Korean        |  zh-tw - Chinese (Traditional)
fr - French         |  ar - Arabic        |  hi - Hindi
de - German         |  tr - Turkish       |  pt - Portuguese
it - Italian        |  ru - Russian
```

---

## 🎯 Next Steps

- **GUI Users:** Read [GUI_USER_GUIDE.md](GUI_USER_GUIDE.md) for detailed features
- **Developers:** Check [GUI_DEVELOPER_GUIDE.md](GUI_DEVELOPER_GUIDE.md) for customization
- **All Users:** See [README.md](README.md) for complete documentation
- **Examples:** View [examples.py](examples.py) for code samples

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| GUI won't open | Ensure tkinter is installed (usually built-in with Python) |
| Port 5000 in use | Change port in `app.py`: `app.run(debug=True, port=5001)` |
| Connection timeout | Check internet connection (needed for Google Translate) |
| Bad language detection | Use longer text for better accuracy |
| History not saving | Check file permissions in application directory |

---

**Happy translating! 🌍✨**
