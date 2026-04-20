# Python Translator 🌍

A powerful Python translation application with **CLI**, **Web UI**, and **REST API**. Supports 14+ languages with auto-detection and real-time translation.

## ✨ Features

- ✅ **Multiple Language Support** - 14+ languages including English, Spanish, French, German, Japanese, Chinese, Hindi, Arabic, etc.
- ✅ **Auto-Detection** - Automatically detect input language
- ✅ **CLI Interface** - Command-line translation with interactive mode
- ✅ **Desktop GUI** - Beautiful Tkinter GUI with translation and history windows
- ✅ **Web Interface** - Responsive web UI with real-time translation
- ✅ **REST API** - Full-featured REST API for programmatic access
- ✅ **Error Handling** - Comprehensive error messages and validation
- ✅ **Translation History** - Automatic tracking and export of translations
- ✅ **API Testing Suite** - Complete test suite for API endpoints

## 📦 Installation

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Setup

1. **Navigate to the project directory:**
   ```bash
   cd translator
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Option 1: Desktop GUI (Recommended for Users)

**Launch the GUI application:**
```bash
python gui.py
```

**Features:**
- 🖥️ Professional desktop interface
- 📝 Input and output text windows
- 📜 Translation history panel
- 🔄 Swap languages instantly
- 📋 Copy/paste functionality
- 💾 Auto-save translation history
- 📤 Export history as JSON
- ⌨️ Keyboard shortcuts (Ctrl+Enter to translate)

**Quick Start:**
1. Select source and destination languages
2. Enter text in the input window
3. Click "TRANSLATE" or press Ctrl+Enter
4. View result in output window
5. History automatically saved for future reference

---

### Option 2: Command Line Interface (CLI)

**Run interactive translator:**
```bash
python translator.py
```

**Translate directly from command line:**
```bash
python translator.py "Hello" en es
```

**Quick examples:**
```bash
python translator.py "Good morning" en fr        # English to French
python translator.py "Bonjour" fr en             # French to English  
python translator.py "こんにちは"                # Auto-detect to English
python translator.py "Hola" es de                # Spanish to German
```

---

### Option 3: Web Interface

**Start the Flask server:**
```bash
python app.py
```

Then open your browser to: `http://localhost:5000`

Features:
- Real-time translation
- Language auto-detection with confidence score
- Clean, intuitive UI
- Responsive design

---

### Option 4: REST API

**Start the Flask server:**
```bash
python app.py
```

## 📡 API Reference

### 1. Translate Text
**Endpoint:** `POST /api/translate`

**Request:**
```json
{
  "text": "Hello World",
  "source_lang": "en",
  "dest_lang": "es"
}
```

**Response:**
```json
{
  "success": true,
  "original": "Hello World",
  "translated": "Hola Mundo",
  "source_lang": "en",
  "dest_lang": "es",
  "timestamp": "2026-04-20T10:30:45.123456"
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "source_lang": "en", "dest_lang": "es"}'
```

---

### 2. Detect Language
**Endpoint:** `POST /api/detect`

**Request:**
```json
{
  "text": "Bonjour"
}
```

**Response:**
```json
{
  "success": true,
  "text": "Bonjour",
  "language": "French",
  "code": "fr",
  "confidence": 0.95,
  "timestamp": "2026-04-20T10:30:45.123456"
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Bonjour"}'
```

---

### 3. Get Supported Languages
**Endpoint:** `GET /api/languages`

**Response:**
```json
{
  "success": true,
  "languages": {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    ...
  },
  "total": 14
}
```

**Example with curl:**
```bash
curl http://localhost:5000/api/languages
```

---

### 4. Health Check
**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "success": true,
  "status": "healthy",
  "service": "Python Translator API",
  "timestamp": "2026-04-20T10:30:45.123456"
}
```

---

## 🗣️ Supported Languages

| Code | Language |
|------|----------|
| en | English |
| es | Spanish |
| fr | French |
| de | German |
| it | Italian |
| pt | Portuguese |
| ru | Russian |
| ja | Japanese |
| ko | Korean |
| zh-cn | Chinese (Simplified) |
| zh-tw | Chinese (Traditional) |
| hi | Hindi |
| ar | Arabic |
| tr | Turkish |

## 🧪 Testing

### Test API with Python Script
```bash
python test_api.py
```

The test suite includes:
- Health check testing
- Language list validation
- Translation accuracy testing
- Language detection testing
- Error handling verification

### Manual Testing with curl
```bash
# Health check
curl http://localhost:5000/api/health

# Get languages
curl http://localhost:5000/api/languages

# Translate
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "source_lang": "en", "dest_lang": "es"}'

# Detect
curl -X POST http://localhost:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Bonjour"}'
```

## 📋 Project Structure

```
translator/
├── translator.py          # Core translator class and CLI
├── app.py                 # Flask web server with REST API
├── test_api.py            # API test suite
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Web interface
└── README.md             # This file
```

## 🔧 Usage Examples

### Python Code Integration
```python
from translator import SimpleTranslator

translator = SimpleTranslator()

# Translate text
result = translator.translate("Hello World", src_lang="en", dest_lang="es")
print(result)
# Output: {'success': True, 'original': 'Hello World', 'translated': 'Hola Mundo', ...}

# Detect language
detection = translator.detect_language("Bonjour")
print(detection)
# Output: {'success': True, 'language': 'French', 'code': 'fr', 'confidence': 0.95}

# Get supported languages
languages = translator.list_languages()
```

### JavaScript/Web Integration
```javascript
// Translate using fetch API
const response = await fetch('/api/translate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    text: 'Hello',
    source_lang: 'en',
    dest_lang: 'es'
  })
});

const data = await response.json();
console.log(data.translated);  // "Hola"
```

## 🛠️ Troubleshooting

### Issue: ModuleNotFoundError
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution:** Change port in `app.py`
```python
app.run(debug=True, port=5001)  # Use different port
```

### Issue: Connection timeout
**Solution:** Check internet connection (needed for Google Translate API)

### Issue: Language detection inaccurate
**Solution:** Use longer text for better detection accuracy

## 📝 Requirements

```
googletrans==4.0.0rc1
Flask==2.3.0
requests==2.31.0  (for testing)
```

## 🤝 API Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Text cannot be empty"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Endpoint not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Translation error: [detailed error message]"
}
```

## 📄 License

MIT License - Feel free to use this project for any purpose.

## 🎯 Features Roadmap

- [x] ✅ Desktop GUI with translation windows
- [x] ✅ Translation history with export
- [x] ✅ CLI interface
- [x] ✅ Web interface
- [x] ✅ REST API
- [ ] Batch translation
- [ ] Document translation (PDF, DOCX)
- [ ] Speech-to-text integration
- [ ] Database for storing translations
- [ ] Dark/Light theme switcher

## 📚 Documentation

- **[GUI User Guide](GUI_USER_GUIDE.md)** - Complete GUI usage guide
- **[GUI Developer Guide](GUI_DEVELOPER_GUIDE.md)** - Customization and development
- **[Quick Start Guide](QUICKSTART.md)** - 5-minute setup guide
- **[Project Summary](PROJECT_SUMMARY.md)** - Feature breakdown
- **[File Index](FILE_INDEX.md)** - Complete file reference

## 👨‍💻 Contributing

Feel free to fork, modify, and use for your projects!

---

**Happy Translating! 🌍✨**

