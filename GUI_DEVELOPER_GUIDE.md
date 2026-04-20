# 🖥️ Python Translator GUI - Developer Guide

## Overview

The GUI module (`gui.py`) provides a complete Tkinter-based desktop interface for the Python Translator.

---

## 📁 File Structure

**Main GUI File:** `gui.py` (450+ lines)

### Class Structure
```
TranslatorGUI
├── __init__()
├── setup_styles()
├── create_widgets()
├── create_translation_area()
├── create_history_area()
├── create_control_panel()
├── translate_text()
├── detect_language()
├── swap_languages()
├── History Management
│   ├── add_to_history()
│   ├── refresh_history_display()
│   ├── save_history()
│   ├── load_history()
│   └── export_history()
├── Utility Methods
│   ├── clear_input()
│   ├── clear_output()
│   ├── copy_output()
│   └── paste_input()
└── Dialog Methods
    ├── show_settings()
    ├── show_help()
    └── show_about()
```

---

## 🎨 Customization Guide

### Colors

Edit colors in `setup_styles()` method (lines 40-46):

```python
def setup_styles(self):
    """Setup colors and fonts"""
    self.bg_color = "#f0f0f0"           # Background color
    self.primary_color = "#667eea"      # Primary button color (purple)
    self.secondary_color = "#764ba2"    # Secondary color (dark purple)
    self.success_color = "#4caf50"      # Success message color (green)
    self.error_color = "#f44336"        # Error message color (red)
    self.text_color = "#333333"         # Text color (dark gray)
```

**Color Palette Examples:**

Dark Theme:
```python
self.bg_color = "#1e1e1e"
self.primary_color = "#bb86fc"
self.secondary_color = "#03dac6"
self.success_color = "#4caf50"
self.error_color = "#ff6b6b"
self.text_color = "#ffffff"
```

Light Theme (Current):
```python
self.bg_color = "#f0f0f0"
self.primary_color = "#667eea"
self.secondary_color = "#764ba2"
self.success_color = "#4caf50"
self.error_color = "#f44336"
self.text_color = "#333333"
```

Professional Blue:
```python
self.bg_color = "#ecf0f1"
self.primary_color = "#3498db"
self.secondary_color = "#2980b9"
self.success_color = "#27ae60"
self.error_color = "#e74c3c"
self.text_color = "#2c3e50"
```

---

### Fonts

Edit fonts in `setup_styles()` method (lines 47-50):

```python
self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
self.label_font = tkFont.Font(family="Helvetica", size=10, weight="bold")
self.button_font = tkFont.Font(family="Helvetica", size=9)
self.text_font = tkFont.Font(family="Courier New", size=10)
```

**Font Options:**
```python
# Common Fonts: "Helvetica", "Arial", "Times New Roman", "Courier New"
# Mac Fonts: "Monaco", "Menlo"
# Linux Fonts: "DejaVu Sans", "Liberation Mono"

# Sizes: 8-14 recommended for GUI
# Weights: "normal", "bold"
```

---

### Window Size

Edit in `__init__()` method (line 12):

```python
self.root.geometry("1200x700")  # Width x Height
```

**Common Sizes:**
```python
self.root.geometry("800x600")    # Smaller (netbook)
self.root.geometry("1024x768")   # Laptop
self.root.geometry("1200x700")   # Desktop (current)
self.root.geometry("1400x900")   # Large screen
```

---

## 🔧 Adding New Features

### Add a New Button

Example: Add "Statistics" button to control panel

```python
def create_control_panel(self, parent):
    """Create main control panel"""
    control_frame = ttk.LabelFrame(...)
    
    # ... existing buttons ...
    
    # New button
    ttk.Button(
        control_frame,
        text="📊 Statistics",
        command=self.show_statistics
    ).pack(side=tk.LEFT, padx=5)

def show_statistics(self):
    """Show translation statistics"""
    messagebox.showinfo(
        "Statistics",
        f"Total Translations: {len(self.history)}\n"
        f"Most Used Language: English\n"
        f"Total Characters: 15000"
    )
```

### Add a New Text Feature

Example: Add word count indicator

```python
def create_translation_area(self, parent):
    # ... existing code ...
    
    # Add word count label
    self.word_count_label = tk.Label(
        trans_frame,
        text="Words: 0 | Chars: 0",
        font=tkFont.Font(family="Helvetica", size=9),
        bg=self.bg_color,
        fg="#666666"
    )
    self.word_count_label.pack(anchor=tk.W, pady=5)
    
    # Bind text update event
    self.input_text.bind('<KeyRelease>', self.update_word_count)

def update_word_count(self, event=None):
    """Update word and character count"""
    text = self.input_text.get("1.0", tk.END)
    words = len(text.split())
    chars = len(text.strip())
    self.word_count_label.config(
        text=f"Words: {words} | Chars: {chars}"
    )
```

### Add a Settings Option

Example: Add theme switcher

```python
def show_settings(self):
    """Show settings dialog"""
    # Create settings window
    settings_window = tk.Toplevel(self.root)
    settings_window.title("Settings")
    settings_window.geometry("300x200")
    
    # Theme selection
    ttk.Label(settings_window, text="Theme:").pack(pady=10)
    theme_var = tk.StringVar(value="light")
    ttk.Radiobutton(settings_window, text="Light", 
                    variable=theme_var, value="light").pack()
    ttk.Radiobutton(settings_window, text="Dark", 
                    variable=theme_var, value="dark").pack()
    
    # Save button
    ttk.Button(
        settings_window,
        text="Apply",
        command=lambda: self.apply_theme(theme_var.get())
    ).pack(pady=10)

def apply_theme(self, theme):
    """Apply theme"""
    if theme == "dark":
        self.bg_color = "#1e1e1e"
        self.primary_color = "#bb86fc"
        # Update all widgets...
    messagebox.showinfo("Theme", f"{theme.capitalize()} theme applied!")
```

---

## 🧪 Testing Features

### Test Translation
```python
def test_translation():
    """Test translation feature"""
    root = tk.Tk()
    app = TranslatorGUI(root)
    
    # Set input text
    app.input_text.insert("1.0", "Hello")
    app.source_lang_var.set("auto")
    app.dest_lang_var.set("en - English")
    
    # Trigger translation
    app.translate_text()
    
    # Check output
    output = app.output_text.get("1.0", tk.END)
    assert output.strip() != ""
    print("✅ Translation test passed")
```

### Test History
```python
def test_history():
    """Test history feature"""
    root = tk.Tk()
    app = TranslatorGUI(root)
    
    # Add items to history
    app.add_to_history("Hello", "Hola", "en", "es")
    app.add_to_history("Good morning", "Buen día", "en", "es")
    
    # Check history length
    assert len(app.history) == 2
    print("✅ History test passed")
```

---

## 📦 Dependencies

### Built-in Libraries
- `tkinter` - GUI framework (included with Python)
- `tkinter.ttk` - Modern widgets
- `tkinter.scrolledtext` - Scrolled text widget
- `tkinter.filedialog` - File selection dialogs
- `tkinter.messagebox` - Message dialogs
- `tkinter.font` - Font handling
- `json` - History serialization
- `os` - File operations
- `datetime` - Timestamps

### External Dependencies
- `translator.SimpleTranslator` - Translation logic

**Note:** No additional pip packages needed for GUI!

---

## 🔌 Integration Points

### With Main Translator
```python
from translator import SimpleTranslator

# Initialize
self.translator = SimpleTranslator()

# Use translate method
result = self.translator.translate(text, src_lang=src, dest_lang=dest)

# Use detect method
detection = self.translator.detect_language(text)

# Get languages
self.languages = self.translator.list_languages()
```

---

## 🎯 Performance Optimization

### Optimize for Large Texts
```python
def translate_text(self):
    """Optimized translation for large texts"""
    text = self.input_text.get("1.0", tk.END).strip()
    
    # Split if too long (e.g., > 1000 chars)
    if len(text) > 1000:
        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
        results = []
        
        for chunk in chunks:
            result = self.translator.translate(chunk, ...)
            if result['success']:
                results.append(result['translated'])
        
        full_translation = " ".join(results)
        # Display combined results
```

### Cache Translations
```python
def __init__(self, root):
    # ... existing code ...
    self.translation_cache = {}  # New: Cache for translations

def translate_text(self):
    # Check cache first
    cache_key = f"{text}:{src_code}:{dest_code}"
    if cache_key in self.translation_cache:
        result = self.translation_cache[cache_key]
    else:
        result = self.translator.translate(...)
        self.translation_cache[cache_key] = result
```

---

## 🐛 Debugging

### Enable Debug Mode

```python
DEBUG = True

def debug_print(message):
    if DEBUG:
        print(f"[DEBUG] {message}")

# Use in methods
def translate_text(self):
    debug_print(f"Translating: {text[:50]}...")
    result = self.translator.translate(...)
    debug_print(f"Result: {result}")
```

### Log Errors
```python
def save_error_log(self, error_msg):
    """Save error to log file"""
    with open("translator_errors.log", "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {error_msg}\n")

# Use in exception handlers
except Exception as e:
    self.save_error_log(str(e))
    messagebox.showerror("Error", str(e))
```

---

## 🚀 Future Enhancements

### Planned Features
- [ ] Drag & drop file import
- [ ] Real-time translation (as you type)
- [ ] Speech input/output
- [ ] Dictionary lookup
- [ ] Translation memory
- [ ] Project management
- [ ] Batch file translation
- [ ] Dark/Light theme switcher
- [ ] Customizable shortcuts
- [ ] Multi-window support

### Code Structure for Features
```python
# Speech module
class SpeechModule:
    def text_to_speech(self, text, language):
        pass
    
    def speech_to_text(self):
        pass

# Dictionary module
class DictionaryModule:
    def lookup_word(self, word, language):
        pass

# Integrate in TranslatorGUI
def __init__(self, root):
    self.translator = SimpleTranslator()
    self.speech = SpeechModule()  # New
    self.dictionary = DictionaryModule()  # New
```

---

## 📊 Code Statistics

- **Total Lines:** 450+
- **Methods:** 30+
- **Classes:** 1 (TranslatorGUI)
- **GUI Elements:** 20+
- **Configuration Options:** 50+

---

## 🎓 Learning Resources

### Understanding Tkinter
- Tkinter official documentation
- GUI layout systems (Grid, Pack, Place)
- Event binding and callbacks
- Custom widgets and styling

### Related Reading
- Python GUI Programming with Tkinter
- Tkinter Best Practices
- Desktop Application Design Patterns

---

**Version:** 1.0  
**Last Updated:** April 20, 2026  
**Status:** Production Ready ✅
