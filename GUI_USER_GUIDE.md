# 🖥️ Python Translator GUI - User Guide

## Overview

The Python Translator now includes a professional desktop GUI application with:
- ✅ **Translation Window** - Input and output text areas
- ✅ **Language Selection** - 14+ language support with swap functionality
- ✅ **Translation History** - Track and manage all translations
- ✅ **Advanced Features** - Copy, paste, detect, export, and more
- ✅ **Modern Design** - Responsive and user-friendly interface

---

## 🚀 Getting Started

### Launch the GUI
```bash
python gui.py
```

The application window will open with all components ready to use.

---

## 📋 User Interface Components

### 1. **Language Selection Panel**
Located at the top of the window:
- **From:** Select source language (default: auto-detect)
- **Swap Button (⇄):** Quickly swap source and destination languages
- **To:** Select destination language (default: English)

### 2. **Translation Input Window**
Large text area for entering text to translate:
- Supports multi-line input
- Word wrapping enabled
- Character count displayed in status bar

**Input Buttons:**
- **Clear Input** - Empty the input field
- **Paste** - Paste from clipboard (Ctrl+V)
- **Detect Language** - Detect input language automatically

### 3. **Translation Output Window**
Displays translated text (read-only):
- Real-time translation results
- Formatted and readable output
- Character count shown

**Output Buttons:**
- **Copy Output** - Copy to clipboard (Ctrl+C)
- **Clear Output** - Empty the output field

### 4. **Translation History Panel**
Right side of the window showing:
- All previous translations with timestamps
- Source and destination languages
- Original text preview
- Sorted by most recent first

**History Features:**
- **Load Selected** - Reload a previous translation
- **Delete Selected** - Remove a specific history item
- **Clear All** - Remove all history
- **Export** - Save history to JSON file

### 5. **Control Panel**
Bottom section with main controls:
- **TRANSLATE** - Main button to translate text
- **Settings** - App settings (coming soon features)
- **Help** - Usage guide and information
- **About** - Application information

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl+Enter** | Translate text |
| **Ctrl+D** | Detect language |
| **Ctrl+C** | Copy output |

---

## 🎯 Usage Guide

### Step 1: Select Languages
1. Click the "From:" dropdown and select source language
   - Choose "auto" for automatic language detection
   - Or select a specific language code
2. Click the "To:" dropdown and select destination language

### Step 2: Enter Text
1. Click in the input window
2. Type or paste text to translate
3. Text can be single or multiple lines

### Step 3: Translate
1. Click the **"TRANSLATE"** button (or press Ctrl+Enter)
2. Wait for the translation to complete
3. Result appears in the output window
4. Translation is automatically added to history

### Step 4: Review & Export
1. Use translation history to review previous translations
2. Click "Load Selected" to reload any translation
3. Click "Export" to save history as JSON file

---

## 📜 Translation History

### Automatic Saving
- Every translation is automatically saved to `translator_history.json`
- Maximum 100 most recent translations stored
- Persists between application sessions

### History Operations

**Load Previous Translation:**
1. Click on any item in the history list
2. Input and output text automatically populate
3. Language selectors update automatically

**Delete History Item:**
1. Select the item in the history list
2. Click "Delete Selected"
3. Confirm the deletion

**Clear All History:**
1. Click "Clear All" button
2. Confirm the action
3. All history is removed

**Export History:**
1. Click "Export" button
2. Choose location and filename
3. History saved as formatted JSON file
4. Can be opened in any text editor or spreadsheet

### History Format
```json
[
  {
    "timestamp": "2026-04-20 10:30:45",
    "original": "Hello, how are you?",
    "translated": "¿Hola, cómo estás?",
    "src_lang": "en",
    "dest_lang": "es"
  }
]
```

---

## 🔧 Features & Functions

### Language Detection
**Automatic Detection:**
- Click "Detect Language" button
- System analyzes input text
- Detected language shown in popup
- Confidence score displayed
- Source language automatically updated

### Swap Languages
**Quick Language Switch:**
1. Click the "⇄ Swap" button
2. Source and destination languages swap
3. Input and output text swap positions
4. Perfect for reverse translation

### Copy & Paste
**Clipboard Operations:**
- **Paste:** Click "Paste" button to paste from clipboard
- **Copy:** Click "Copy Output" to copy translation to clipboard
- Status bar confirms operations

### Status Bar
Located at bottom of translation area:
- Shows current operation status
- Character count of translations
- Color-coded messages:
  - 🟢 Green: Success messages
  - 🔴 Red: Error messages
  - 🟠 Orange: In-progress messages

---

## 💾 Data & Settings

### Automatic Data Storage
- Translation history saved automatically
- Located in: `translator_history.json`
- In the same directory as `gui.py`
- Plain text JSON format (human-readable)

### Configuration
- **Theme:** Default dark-light (coming soon)
- **Font Size:** Medium (adjustable in code)
- **Auto-save:** Enabled by default
- **History Limit:** 100 items maximum

### Modifying Settings
Edit `gui.py` to customize:
```python
# Colors (line ~40)
self.primary_color = "#667eea"      # Primary button color
self.secondary_color = "#764ba2"    # Secondary button color
self.success_color = "#4caf50"      # Success message color
self.error_color = "#f44336"        # Error message color

# Fonts (line ~47)
self.title_font = tkFont.Font(...)  # Title font
self.label_font = tkFont.Font(...)  # Label font
```

---

## 🌐 Supported Languages

All 14 languages are supported:

**European:**
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Turkish (tr)

**Asian:**
- Japanese (ja)
- Korean (ko)
- Chinese Simplified (zh-cn)
- Chinese Traditional (zh-tw)
- Hindi (hi)

**Middle Eastern:**
- Arabic (ar)

---

## 🎨 User Interface Details

### Window Size
- **Default:** 1200x700 pixels
- **Resizable:** Yes
- **Minimum:** Adaptable to smaller screens
- **Maximum:** Can be maximized

### Colors & Theme
- **Background:** Light gray (#f0f0f0)
- **Primary:** Purple (#667eea)
- **Secondary:** Dark purple (#764ba2)
- **Success:** Green (#4caf50)
- **Error:** Red (#f44336)

### Layout
- **Left 60%:** Translation area (input + output)
- **Right 40%:** History panel
- **Bottom 15%:** Control panel

---

## 📱 Common Tasks

### Translate a Short Phrase
1. Type phrase in input
2. Click TRANSLATE
3. View result in output
4. Click "Copy Output" to use elsewhere

### Translate a Long Document
1. Paste entire text in input
2. Select languages
3. Click TRANSLATE
4. Export from history for archival

### Compare Multiple Translations
1. Load translation from history
2. Change destination language
3. Click TRANSLATE again
4. Compare results

### Build Multilingual Dictionary
1. Enter word/phrase
2. Translate to multiple languages
3. Use "Swap" to reverse
4. Export history when complete

---

## ⚠️ Troubleshooting

### GUI Won't Open
```bash
# Check if tkinter is installed (usually built-in)
python -m tkinter

# If error, install tkinter:
# On Windows: Usually included with Python
# On Linux: sudo apt-get install python3-tk
# On Mac: Should be included with Python
```

### Text Not Translating
- Ensure internet connection is active
- Check language codes are correct
- Try entering longer text (short text might be detected incorrectly)
- Check status bar for error messages

### History Not Saving
- Ensure write permissions in application directory
- Check `translator_history.json` file is not corrupted
- Delete `translator_history.json` to start fresh

### Slow Translation
- Network latency (Internet connection)
- Very long text (split into smaller chunks)
- System resources (close other applications)

---

## 🔐 Privacy & Data

### Data Storage
- All translations stored locally in `translator_history.json`
- No data sent to external servers (except Google Translate API)
- User has full control over history (can delete anytime)

### Export Privacy
- Exported JSON files contain only translation data
- No metadata about user stored
- Files can be shared, deleted, or archived as needed

---

## 🚀 Advanced Features

### Settings Dialog
Click "Settings" to view:
- Theme options (coming soon)
- Font size adjustments (coming soon)
- Auto-save settings
- Maximum history items
- All keyboard shortcuts

### Help Dialog
Click "Help" for:
- Quick start guide
- Feature list
- Supported languages
- System information

### About Dialog
Click "About" for:
- Application version
- Technology stack
- Credits and attribution
- License information

---

## 📊 System Requirements

### Minimum
- Python 3.7+
- 50 MB disk space
- Internet connection for translation

### Recommended
- Python 3.8+
- 100 MB disk space
- High-speed internet connection
- Modern operating system

### Operating Systems
- ✅ Windows 7+
- ✅ macOS 10.12+
- ✅ Linux (Ubuntu, Debian, CentOS, etc.)

---

## 🎯 Tips & Tricks

### Pro Tips
1. **Use Auto-Detect:** Let the system detect language for faster translation
2. **Swap Feature:** Perfect for comparing original and translation
3. **History Search:** Scroll through history to find similar translations
4. **Export Regularly:** Save important translations periodically
5. **Multi-line:** Use for translating paragraphs and documents

### Best Practices
- Keep translations under 1000 characters for best speed
- Use specific language selection for technical terms
- Test with similar text first before large translations
- Export history before closing application for backup
- Clear history periodically to save space

---

## 📞 Support & Feedback

### Common Issues
- **Issue:** GUI closes unexpectedly
  - **Solution:** Check Python version compatibility

- **Issue:** History not loading
  - **Solution:** Delete corrupted history file, restart app

- **Issue:** Translations taking too long
  - **Solution:** Check internet connection speed

---

## 🎉 Features Summary

✅ **Complete Translation Interface**
✅ **14+ Languages Supported**
✅ **Automatic History Tracking**
✅ **Export/Import Functionality**
✅ **Keyboard Shortcuts**
✅ **Copy/Paste Support**
✅ **Language Detection**
✅ **Swap Functionality**
✅ **Responsive Design**
✅ **Modern UI with Colors**
✅ **Status Indicators**
✅ **Help & Settings Dialogs**

---

**Last Updated:** April 20, 2026
**Version:** 1.0
**Status:** Production Ready ✅
