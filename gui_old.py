#!/usr/bin/env python3
"""
Advanced Python Translator GUI Application
Professional desktop interface with modern design and advanced features
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import tkinter.font as tkFont
from translator import SimpleTranslator
import json
import os
from datetime import datetime
import threading

class ModernTranslatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Translator 🌍")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Initialize translator
        self.translator = SimpleTranslator()
        self.languages = self.translator.list_languages()
        
        # History list
        self.history = []
        self.load_history()
        
        # Set up colors and fonts
        self.setup_styles()
        
        # Create GUI
        self.create_widgets()
        
        # Bind keyboard shortcuts
        self.setup_shortcuts()
    
    def setup_styles(self):
        """Setup colors and fonts"""
        self.bg_color = "#f0f0f0"
        self.primary_color = "#667eea"
        self.secondary_color = "#764ba2"
        self.success_color = "#4caf50"
        self.error_color = "#f44336"
        self.text_color = "#333333"
        
        self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=10, weight="bold")
        self.button_font = tkFont.Font(family="Helvetica", size=9)
        self.text_font = tkFont.Font(family="Courier New", size=10)
        
        self.root.configure(bg=self.bg_color)
    
    def create_widgets(self):
        """Create GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🌍 Python Translator",
            font=self.title_font,
            bg=self.bg_color,
            fg=self.primary_color
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Create main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=10)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Left side - Translation area
        self.create_translation_area(content_frame)
        
        # Right side - History
        self.create_history_area(content_frame)
        
        # Bottom - Control panel
        self.create_control_panel(main_frame)
    
    def create_translation_area(self, parent):
        """Create translation input/output area"""
        # Main translation frame
        trans_frame = ttk.Frame(parent)
        trans_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Language selection row
        lang_frame = ttk.Frame(trans_frame)
        lang_frame.pack(fill=tk.X, pady=10)
        
        # Source language
        ttk.Label(lang_frame, text="From:", font=self.label_font).pack(side=tk.LEFT, padx=5)
        self.source_lang_var = tk.StringVar(value="auto")
        source_combo = ttk.Combobox(
            lang_frame, 
            textvariable=self.source_lang_var,
            values=["auto"] + [f"{code} - {name}" for code, name in self.languages.items()],
            width=25,
            state="readonly"
        )
        source_combo.pack(side=tk.LEFT, padx=5)
        
        # Swap button
        swap_btn = tk.Button(
            lang_frame,
            text="⇄ Swap",
            command=self.swap_languages,
            font=self.button_font,
            bg=self.secondary_color,
            fg="white",
            padx=10
        )
        swap_btn.pack(side=tk.LEFT, padx=5)
        
        # Destination language
        ttk.Label(lang_frame, text="To:", font=self.label_font).pack(side=tk.LEFT, padx=5)
        self.dest_lang_var = tk.StringVar(value="en - English")
        dest_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.dest_lang_var,
            values=[f"{code} - {name}" for code, name in self.languages.items()],
            width=25,
            state="readonly"
        )
        dest_combo.pack(side=tk.LEFT, padx=5)
        
        # Input area
        input_label = tk.Label(
            trans_frame,
            text="Text to Translate:",
            font=self.label_font,
            bg=self.bg_color
        )
        input_label.pack(anchor=tk.W, pady=(10, 5))
        
        # Input text box
        self.input_text = scrolledtext.ScrolledText(
            trans_frame,
            height=10,
            width=50,
            font=self.text_font,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Input buttons
        input_btn_frame = ttk.Frame(trans_frame)
        input_btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            input_btn_frame,
            text="Clear Input",
            command=self.clear_input
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            input_btn_frame,
            text="Paste",
            command=self.paste_input
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            input_btn_frame,
            text="Detect Language",
            command=self.detect_language
        ).pack(side=tk.LEFT, padx=5)
        
        # Output area
        output_label = tk.Label(
            trans_frame,
            text="Translated Text:",
            font=self.label_font,
            bg=self.bg_color
        )
        output_label.pack(anchor=tk.W, pady=(10, 5))
        
        # Output text box
        self.output_text = scrolledtext.ScrolledText(
            trans_frame,
            height=10,
            width=50,
            font=self.text_font,
            wrap=tk.WORD,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Output buttons
        output_btn_frame = ttk.Frame(trans_frame)
        output_btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            output_btn_frame,
            text="Copy Output",
            command=self.copy_output
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            output_btn_frame,
            text="Clear Output",
            command=self.clear_output
        ).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(
            trans_frame,
            text="Ready",
            font=tkFont.Font(family="Helvetica", size=9),
            bg=self.bg_color,
            fg="#666666"
        )
        self.status_label.pack(anchor=tk.W, pady=5)
    
    def create_history_area(self, parent):
        """Create translation history area"""
        # History frame
        hist_frame = ttk.LabelFrame(
            parent,
            text="📜 Translation History",
            padding=10
        )
        hist_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # History listbox with scrollbar
        scrollbar = ttk.Scrollbar(hist_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(
            hist_frame,
            yscrollcommand=scrollbar.set,
            font=tkFont.Font(family="Courier New", size=8),
            bg="white",
            fg=self.text_color
        )
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # History selection binding
        self.history_listbox.bind('<<ListboxSelect>>', self.on_history_select)
        
        # History buttons
        hist_btn_frame = ttk.Frame(hist_frame)
        hist_btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            hist_btn_frame,
            text="Load Selected",
            command=self.load_from_history
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            hist_btn_frame,
            text="Delete Selected",
            command=self.delete_from_history
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            hist_btn_frame,
            text="Clear All",
            command=self.clear_all_history
        ).pack(side=tk.LEFT, padx=5)
        
        # Export button
        ttk.Button(
            hist_btn_frame,
            text="Export",
            command=self.export_history
        ).pack(side=tk.LEFT, padx=5)
        
        # Refresh history display
        self.refresh_history_display()
    
    def create_control_panel(self, parent):
        """Create main control panel"""
        control_frame = ttk.LabelFrame(
            parent,
            text="⚙️ Controls",
            padding=10
        )
        control_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=10)
        
        # Main translate button
        translate_btn = tk.Button(
            control_frame,
            text="📤 TRANSLATE",
            command=self.translate_text,
            font=tkFont.Font(family="Helvetica", size=12, weight="bold"),
            bg=self.primary_color,
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        translate_btn.pack(side=tk.LEFT, padx=10)
        
        # Settings button
        ttk.Button(
            control_frame,
            text="⚙️ Settings",
            command=self.show_settings
        ).pack(side=tk.LEFT, padx=5)
        
        # Help button
        ttk.Button(
            control_frame,
            text="❓ Help",
            command=self.show_help
        ).pack(side=tk.LEFT, padx=5)
        
        # About button
        ttk.Button(
            control_frame,
            text="ℹ️ About",
            command=self.show_about
        ).pack(side=tk.LEFT, padx=5)
    
    def translate_text(self):
        """Translate the input text"""
        text = self.input_text.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Empty Input", "Please enter text to translate")
            return
        
        # Get language codes
        source_lang = self.source_lang_var.get()
        if source_lang == "auto":
            src_code = "auto"
        else:
            src_code = source_lang.split(" - ")[0]
        
        dest_lang = self.dest_lang_var.get()
        dest_code = dest_lang.split(" - ")[0]
        
        # Translate
        try:
            self.status_label.config(text="Translating...", fg="#FF9800")
            self.root.update()
            
            result = self.translator.translate(text, src_lang=src_code, dest_lang=dest_code)
            
            if result['success']:
                # Display output
                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", result['translated'])
                self.output_text.config(state=tk.DISABLED)
                
                # Add to history
                self.add_to_history(
                    text,
                    result['translated'],
                    src_code,
                    dest_code
                )
                
                self.status_label.config(
                    text=f"✅ Translated successfully ({len(result['translated'])} chars)",
                    fg=self.success_color
                )
            else:
                self.status_label.config(
                    text=f"❌ Error: {result['error']}",
                    fg=self.error_color
                )
                messagebox.showerror("Translation Error", result['error'])
        
        except Exception as e:
            self.status_label.config(
                text=f"❌ Error: {str(e)}",
                fg=self.error_color
            )
            messagebox.showerror("Error", f"Translation failed: {str(e)}")
    
    def detect_language(self):
        """Detect the language of input text"""
        text = self.input_text.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Empty Input", "Please enter text to detect")
            return
        
        try:
            result = self.translator.detect_language(text)
            
            if result['success']:
                lang = result['language']
                code = result['code']
                confidence = result['confidence']
                
                # Update source language selector
                for item in [f"{code} - {name}" for code_check, name in self.languages.items() if code_check == code]:
                    self.source_lang_var.set(item)
                    break
                
                confidence_str = f"{confidence*100:.1f}%" if confidence else "N/A"
                msg = f"Detected Language: {lang} ({code})\nConfidence: {confidence_str}"
                messagebox.showinfo("Language Detection", msg)
                self.status_label.config(
                    text=f"Detected: {lang}",
                    fg=self.success_color
                )
            else:
                messagebox.showerror("Detection Error", result['error'])
        
        except Exception as e:
            messagebox.showerror("Error", f"Detection failed: {str(e)}")
    
    def swap_languages(self):
        """Swap source and destination languages"""
        source = self.source_lang_var.get()
        dest = self.dest_lang_var.get()
        
        if source == "auto":
            messagebox.showinfo("Info", "Cannot swap with auto-detect. Please select a specific source language.")
            return
        
        self.source_lang_var.set(dest)
        self.dest_lang_var.set(source)
        
        # Swap text areas
        input_text = self.input_text.get("1.0", tk.END).strip()
        self.output_text.config(state=tk.NORMAL)
        output_text = self.output_text.get("1.0", tk.END).strip()
        self.output_text.config(state=tk.DISABLED)
        
        if output_text:
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", output_text)
            
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", input_text)
            self.output_text.config(state=tk.DISABLED)
    
    def add_to_history(self, original, translated, src_lang, dest_lang):
        """Add translation to history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_item = {
            "timestamp": timestamp,
            "original": original,
            "translated": translated,
            "src_lang": src_lang,
            "dest_lang": dest_lang
        }
        
        self.history.insert(0, history_item)
        self.save_history()
        self.refresh_history_display()
    
    def refresh_history_display(self):
        """Refresh the history listbox display"""
        self.history_listbox.delete(0, tk.END)
        
        for item in self.history[:50]:  # Show last 50 items
            display_text = f"{item['timestamp']} | {item['src_lang']}->{item['dest_lang']}: {item['original'][:40]}"
            self.history_listbox.insert(tk.END, display_text)
    
    def on_history_select(self, event):
        """Handle history selection"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.history):
                item = self.history[index]
                
                # Display in text areas
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", item['original'])
                
                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", item['translated'])
                self.output_text.config(state=tk.DISABLED)
                
                # Update language selectors
                self.source_lang_var.set(item['src_lang'] if item['src_lang'] != 'auto' else 'auto')
                for code, name in self.languages.items():
                    if code == item['dest_lang']:
                        self.dest_lang_var.set(f"{code} - {name}")
                        break
    
    def load_from_history(self):
        """Load selected history item"""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item from history")
            return
        
        self.on_history_select(None)
    
    def delete_from_history(self):
        """Delete selected history item"""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to delete")
            return
        
        index = selection[0]
        if messagebox.askyesno("Confirm Delete", "Delete this history item?"):
            del self.history[index]
            self.save_history()
            self.refresh_history_display()
            self.status_label.config(text="Item deleted", fg=self.success_color)
    
    def clear_all_history(self):
        """Clear all history"""
        if messagebox.askyesno("Confirm Clear", "Clear all translation history?"):
            self.history = []
            self.save_history()
            self.refresh_history_display()
            self.status_label.config(text="History cleared", fg=self.success_color)
    
    def export_history(self):
        """Export history to JSON file"""
        if not self.history:
            messagebox.showwarning("Empty History", "No history to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.history, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Success", f"History exported to:\n{file_path}")
                self.status_label.config(text="History exported", fg=self.success_color)
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
    
    def clear_input(self):
        """Clear input text"""
        self.input_text.delete("1.0", tk.END)
        self.status_label.config(text="Input cleared", fg="#666666")
    
    def clear_output(self):
        """Clear output text"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.status_label.config(text="Output cleared", fg="#666666")
    
    def copy_output(self):
        """Copy output text to clipboard"""
        output_text = self.output_text.get("1.0", tk.END).strip()
        
        if not output_text:
            messagebox.showwarning("Empty Output", "Nothing to copy")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(output_text)
        self.status_label.config(text="✅ Copied to clipboard", fg=self.success_color)
    
    def paste_input(self):
        """Paste from clipboard to input"""
        try:
            clipboard_text = self.root.clipboard_get()
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", clipboard_text)
            self.status_label.config(text="✅ Pasted from clipboard", fg=self.success_color)
        except Exception as e:
            messagebox.showerror("Paste Error", f"Failed to paste: {str(e)}")
    
    def save_history(self):
        """Save history to file"""
        try:
            history_file = "translator_history.json"
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history[:100], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def load_history(self):
        """Load history from file"""
        try:
            history_file = "translator_history.json"
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
            self.history = []
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-Return>', lambda e: self.translate_text())
        self.root.bind('<Control-d>', lambda e: self.detect_language())
        self.root.bind('<Control-c>', lambda e: self.copy_output())
    
    def show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo(
            "Settings",
            "Settings Options:\n\n"
            "• Theme: Auto (coming soon)\n"
            "• Font Size: Medium (coming soon)\n"
            "• Auto-save History: Enabled\n"
            "• Max History Items: 100\n\n"
            "Keyboard Shortcuts:\n"
            "• Ctrl+Enter: Translate\n"
            "• Ctrl+D: Detect Language\n"
            "• Ctrl+C: Copy Output"
        )
    
    def show_help(self):
        """Show help dialog"""
        messagebox.showinfo(
            "Help",
            "Python Translator - Usage Guide\n\n"
            "1. Enter text in the input field\n"
            "2. Select source and destination languages\n"
            "3. Click 'TRANSLATE' or press Ctrl+Enter\n"
            "4. View translated text in output area\n\n"
            "Features:\n"
            "• Auto-detect language\n"
            "• Swap languages\n"
            "• Copy/paste functionality\n"
            "• Translation history\n"
            "• Export history as JSON\n\n"
            "Supported Languages: 14+\n"
            "Including: English, Spanish, French, German,\n"
            "Japanese, Chinese, Hindi, Arabic, and more"
        )
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            "Python Translator v1.0\n\n"
            "A powerful translation application with:\n"
            "• GUI Desktop Interface\n"
            "• REST API\n"
            "• Command Line Interface\n"
            "• Web Interface\n\n"
            "Powered by Google Translate API\n"
            "Built with Python & Tkinter\n\n"
            "© 2026 - All Rights Reserved"
        )


def main():
    """Main function"""
    root = tk.Tk()
    app = TranslatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
