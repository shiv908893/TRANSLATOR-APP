#!/usr/bin/env python3
"""
Advanced Python Translator GUI Application v2.0
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
        self.root.title("🌍 Advanced Translator v2.0")
        self.root.geometry("1500x850")
        self.root.resizable(True, True)
        self.root.minsize(1100, 650)
        
        # Initialize translator
        self.translator = SimpleTranslator()
        self.languages = self.translator.list_languages()
        
        # History and favorites
        self.history = []
        self.favorites = []
        self.load_data()
        
        # Text statistics
        self.stats = {"chars": 0, "words": 0}
        
        # Theme settings
        self.theme = "light"
        self.setup_styles()
        
        # Create GUI
        self.create_widgets()
        self.setup_shortcuts()
    
    def setup_styles(self):
        """Setup modern colors, fonts, and themes"""
        if self.theme == "light":
            self.bg_color = "#f5f7fa"
            self.fg_color = "#1a1a1a"
            self.card_bg = "#ffffff"
            self.primary_color = "#667eea"
            self.secondary_color = "#764ba2"
            self.success_color = "#10b981"
            self.warning_color = "#f59e0b"
            self.error_color = "#ef4444"
            self.border_color = "#e5e7eb"
        else:  # dark theme
            self.bg_color = "#1e1e2e"
            self.fg_color = "#e0e0e0"
            self.card_bg = "#2d2d44"
            self.primary_color = "#667eea"
            self.secondary_color = "#764ba2"
            self.success_color = "#10b981"
            self.warning_color = "#f59e0b"
            self.error_color = "#ef4444"
            self.border_color = "#404059"
        
        # Font definitions
        self.title_font = tkFont.Font(family="Segoe UI", size=18, weight="bold")
        self.header_font = tkFont.Font(family="Segoe UI", size=12, weight="bold")
        self.label_font = tkFont.Font(family="Segoe UI", size=10, weight="bold")
        self.button_font = tkFont.Font(family="Segoe UI", size=9)
        self.text_font = tkFont.Font(family="Consolas", size=10)
        self.small_font = tkFont.Font(family="Segoe UI", size=8)
        
        self.root.configure(bg=self.bg_color)
    
    def create_widgets(self):
        """Create main GUI structure"""
        # Top header bar
        self.create_header()
        
        # Main content area
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Translation
        self.translation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.translation_frame, text="📝 Translator")
        self.create_translation_tab(self.translation_frame)
        
        # Tab 2: History
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="📜 History & Search")
        self.create_history_tab(self.history_frame)
        
        # Tab 3: Favorites
        self.favorites_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.favorites_frame, text="⭐ Favorites")
        self.create_favorites_tab(self.favorites_frame)
        
        # Tab 4: Statistics
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="📊 Statistics")
        self.create_statistics_tab(self.stats_frame)
        
        # Bottom status bar
        self.create_status_bar()
    
    def create_header(self):
        """Create professional header"""
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Left side - Title
        left_frame = tk.Frame(header_frame, bg=self.primary_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title_label = tk.Label(
            left_frame,
            text="🌍 ADVANCED TRANSLATOR",
            font=self.title_font,
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(
            left_frame,
            text="Professional Translation with Modern Design • 14+ Languages",
            font=tkFont.Font(family="Segoe UI", size=9),
            bg=self.primary_color,
            fg="#e0e7ff"
        )
        subtitle_label.pack(side=tk.LEFT, padx=15)
        
        # Right side - Quick actions
        right_frame = tk.Frame(header_frame, bg=self.primary_color)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=20, pady=10)
        
        theme_btn = tk.Button(
            right_frame,
            text="🌙 Dark Mode",
            command=self.toggle_theme,
            font=self.small_font,
            bg="#8b7dd6",
            fg="white",
            relief=tk.FLAT,
            padx=12,
            pady=6,
            cursor="hand2"
        )
        theme_btn.pack(side=tk.LEFT, padx=5)
        self.theme_btn = theme_btn
    
    def create_translation_tab(self, parent):
        """Create translation main interface"""
        # Language selection card
        lang_card = self.create_card(parent)
        lang_card.pack(fill=tk.X, pady=(0, 10))
        
        lang_inner = tk.Frame(lang_card, bg=self.card_bg)
        lang_inner.pack(fill=tk.X, padx=15, pady=12)
        
        src_label = tk.Label(lang_inner, text="📤 From:", font=self.label_font, bg=self.card_bg, fg=self.fg_color)
        src_label.pack(side=tk.LEFT, padx=5)
        
        self.source_lang_var = tk.StringVar(value="auto (Auto-detect)")
        source_combo = ttk.Combobox(
            lang_inner,
            textvariable=self.source_lang_var,
            values=["auto (Auto-detect)"] + [f"{code} - {name}" for code, name in self.languages.items()],
            width=22,
            state="readonly"
        )
        source_combo.pack(side=tk.LEFT, padx=5)
        
        swap_btn = tk.Button(
            lang_inner,
            text="⇄ SWAP",
            command=self.swap_languages,
            font=self.label_font,
            bg=self.secondary_color,
            fg="white",
            padx=15,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        )
        swap_btn.pack(side=tk.LEFT, padx=10)
        
        dest_label = tk.Label(lang_inner, text="📥 To:", font=self.label_font, bg=self.card_bg, fg=self.fg_color)
        dest_label.pack(side=tk.LEFT, padx=5)
        
        self.dest_lang_var = tk.StringVar(value="en - English")
        dest_combo = ttk.Combobox(
            lang_inner,
            textvariable=self.dest_lang_var,
            values=[f"{code} - {name}" for code, name in self.languages.items()],
            width=22,
            state="readonly"
        )
        dest_combo.pack(side=tk.LEFT, padx=5)
        
        # Main content - three columns
        content_frame = tk.Frame(parent, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Input column
        input_card = self.create_card(content_frame)
        input_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        input_label = tk.Label(
            input_card,
            text="📝 Text to Translate",
            font=self.header_font,
            bg=self.card_bg,
            fg=self.primary_color
        )
        input_label.pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        self.input_text = scrolledtext.ScrolledText(
            input_card,
            height=18,
            font=self.text_font,
            wrap=tk.WORD,
            bg="white" if self.theme == "light" else "#3a3a52",
            fg=self.fg_color,
            relief=tk.FLAT,
            borderwidth=1
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        self.input_text.bind("<KeyRelease>", self.update_stats)
        
        # Stats and buttons
        input_action = tk.Frame(input_card, bg=self.card_bg)
        input_action.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.input_stats_label = tk.Label(
            input_action,
            text="📊 0 characters | 0 words",
            font=self.small_font,
            bg=self.card_bg,
            fg="#999"
        )
        self.input_stats_label.pack(side=tk.LEFT, pady=5)
        
        input_buttons = tk.Frame(input_action, bg=self.card_bg)
        input_buttons.pack(side=tk.RIGHT)
        
        self.create_modern_button(input_buttons, "🔄", self.clear_input, width=3).pack(side=tk.LEFT, padx=2)
        self.create_modern_button(input_buttons, "📋", self.paste_input, width=3).pack(side=tk.LEFT, padx=2)
        
        # Center action buttons
        center_frame = tk.Frame(content_frame, bg=self.bg_color, width=100)
        center_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        center_frame.pack_propagate(False)
        
        # Main translate button
        main_btn = tk.Button(
            center_frame,
            text="✨\nTRANSLATE\n(Ctrl+⏎)",
            command=self.translate_text,
            font=tkFont.Font(family="Segoe UI", size=10, weight="bold"),
            bg=self.primary_color,
            fg="white",
            padx=8,
            pady=18,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.secondary_color
        )
        main_btn.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.create_modern_button(center_frame, "🔍\nDetect", self.detect_language).pack(fill=tk.X, padx=5, pady=2)
        
        # Output column
        output_card = self.create_card(content_frame)
        output_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        output_label = tk.Label(
            output_card,
            text="🎯 Translated Text",
            font=self.header_font,
            bg=self.card_bg,
            fg=self.success_color
        )
        output_label.pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        self.output_text = scrolledtext.ScrolledText(
            output_card,
            height=18,
            font=self.text_font,
            wrap=tk.WORD,
            bg="white" if self.theme == "light" else "#3a3a52",
            fg=self.fg_color,
            state=tk.DISABLED,
            relief=tk.FLAT,
            borderwidth=1
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        # Output action
        output_action = tk.Frame(output_card, bg=self.card_bg)
        output_action.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.output_stats_label = tk.Label(
            output_action,
            text="📊 0 characters | 0 words",
            font=self.small_font,
            bg=self.card_bg,
            fg="#999"
        )
        self.output_stats_label.pack(side=tk.LEFT, pady=5)
        
        output_buttons = tk.Frame(output_action, bg=self.card_bg)
        output_buttons.pack(side=tk.RIGHT)
        
        self.create_modern_button(output_buttons, "❤️", self.add_favorite, width=3).pack(side=tk.LEFT, padx=2)
        self.create_modern_button(output_buttons, "📋", self.copy_output, width=3).pack(side=tk.LEFT, padx=2)
    
    def create_history_tab(self, parent):
        """Create history tab with search"""
        # Search bar
        search_frame = self.create_card(parent)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        search_inner = tk.Frame(search_frame, bg=self.card_bg)
        search_inner.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(search_inner, text="🔍 Search History:", font=self.label_font, bg=self.card_bg, fg=self.fg_color).pack(side=tk.LEFT, padx=5)
        
        self.history_search_var = tk.StringVar()
        self.history_search_var.trace("w", self.filter_history)
        
        search_entry = tk.Entry(
            search_inner,
            textvariable=self.history_search_var,
            font=self.button_font,
            width=40,
            relief=tk.FLAT,
            borderwidth=1
        )
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # History list
        hist_card = self.create_card(parent)
        hist_card.pack(fill=tk.BOTH, expand=True)
        
        hist_inner = tk.Frame(hist_card, bg=self.card_bg)
        hist_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Treeview
        columns = ("Time", "Languages", "Text Preview", "Length")
        self.history_tree = ttk.Treeview(hist_inner, columns=columns, height=20, show="headings")
        
        self.history_tree.column("Time", width=150, anchor=tk.W)
        self.history_tree.column("Languages", width=100, anchor=tk.W)
        self.history_tree.column("Text Preview", width=450, anchor=tk.W)
        self.history_tree.column("Length", width=70, anchor=tk.CENTER)
        
        self.history_tree.heading("Time", text="📅 Time")
        self.history_tree.heading("Languages", text="🌐 Languages")
        self.history_tree.heading("Text Preview", text="📝 Text Preview")
        self.history_tree.heading("Length", text="📏 Len")
        
        scrollbar = ttk.Scrollbar(hist_inner, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_tree.bind("<<TreeviewSelect>>", self.load_from_history_tree)
        
        # Action buttons
        action_frame = tk.Frame(hist_card, bg=self.card_bg)
        action_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.create_modern_button(action_frame, "📤 Load", self.load_from_history).pack(side=tk.LEFT, padx=3)
        self.create_modern_button(action_frame, "🗑️ Delete", self.delete_from_history).pack(side=tk.LEFT, padx=3)
        self.create_modern_button(action_frame, "🧹 Clear All", self.clear_all_history).pack(side=tk.LEFT, padx=3)
        self.create_modern_button(action_frame, "💾 Export", self.export_history).pack(side=tk.LEFT, padx=3)
        
        self.refresh_history_tree()
    
    def create_favorites_tab(self, parent):
        """Create favorites tab"""
        info_frame = self.create_card(parent)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_inner = tk.Frame(info_frame, bg=self.card_bg)
        info_inner.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(info_inner, text="❤️ Save favorite translations for quick access", font=self.label_font, bg=self.card_bg, fg=self.primary_color).pack(side=tk.LEFT)
        
        # Favorites list
        fav_card = self.create_card(parent)
        fav_card.pack(fill=tk.BOTH, expand=True)
        
        fav_inner = tk.Frame(fav_card, bg=self.card_bg)
        fav_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        columns = ("Original", "Translated", "Languages")
        self.favorites_tree = ttk.Treeview(fav_inner, columns=columns, height=20, show="headings")
        
        self.favorites_tree.column("Original", width=350, anchor=tk.W)
        self.favorites_tree.column("Translated", width=350, anchor=tk.W)
        self.favorites_tree.column("Languages", width=120, anchor=tk.W)
        
        self.favorites_tree.heading("Original", text="📝 Original")
        self.favorites_tree.heading("Translated", text="🎯 Translated")
        self.favorites_tree.heading("Languages", text="🌐 Lang")
        
        scrollbar = ttk.Scrollbar(fav_inner, orient=tk.VERTICAL, command=self.favorites_tree.yview)
        self.favorites_tree.configure(yscroll=scrollbar.set)
        
        self.favorites_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.favorites_tree.bind("<<TreeviewSelect>>", self.load_from_favorites_tree)
        
        # Action buttons
        fav_action = tk.Frame(fav_card, bg=self.card_bg)
        fav_action.pack(fill=tk.X, padx=15, pady=10)
        
        self.create_modern_button(fav_action, "📤 Load", self.load_from_favorites).pack(side=tk.LEFT, padx=3)
        self.create_modern_button(fav_action, "🗑️ Remove", self.remove_favorite).pack(side=tk.LEFT, padx=3)
        self.create_modern_button(fav_action, "🧹 Clear All", self.clear_favorites).pack(side=tk.LEFT, padx=3)
        
        self.refresh_favorites_tree()
    
    def create_statistics_tab(self, parent):
        """Create statistics tab"""
        # Stat cards
        cards_frame = tk.Frame(parent, bg=self.bg_color)
        cards_frame.pack(fill=tk.X, pady=10)
        
        for i, (title, icon) in enumerate([
            ("📚 Total Translations", "0"),
            ("❤️ Favorites", "0"),
            ("🌐 Languages Used", "0"),
            ("📊 Avg Text Length", "0")
        ]):
            self.create_stat_card(cards_frame, title, icon, i)
        
        # Detailed stats
        detailed_card = self.create_card(parent)
        detailed_card.pack(fill=tk.BOTH, expand=True, pady=10)
        
        detailed_label = tk.Label(
            detailed_card,
            text="📈 Detailed Statistics & Analytics",
            font=self.header_font,
            bg=self.card_bg,
            fg=self.primary_color
        )
        detailed_label.pack(anchor=tk.W, padx=15, pady=10)
        
        self.stats_text = scrolledtext.ScrolledText(
            detailed_card,
            height=18,
            font=self.text_font,
            wrap=tk.WORD,
            state=tk.DISABLED,
            relief=tk.FLAT
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.update_statistics_display()
    
    def create_stat_card(self, parent, title, value, column):
        """Create stat card"""
        card = self.create_card(parent)
        card.grid(row=0, column=column, sticky="nsew", padx=5)
        parent.grid_columnconfigure(column, weight=1)
        
        card_inner = tk.Frame(card, bg=self.card_bg)
        card_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        tk.Label(card_inner, text=title, font=self.label_font, bg=self.card_bg, fg=self.fg_color).pack(anchor=tk.W)
        
        value_label = tk.Label(
            card_inner,
            text=value,
            font=tkFont.Font(family="Segoe UI", size=24, weight="bold"),
            bg=self.card_bg,
            fg=self.primary_color
        )
        value_label.pack(anchor=tk.W, pady=5)
    
    def create_card(self, parent):
        """Create card widget"""
        card = tk.Frame(
            parent,
            bg=self.card_bg,
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=self.border_color,
            highlightcolor=self.primary_color
        )
        return card
    
    def create_modern_button(self, parent, text, command, width=None):
        """Create modern button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=self.button_font,
            bg=self.primary_color,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor="hand2",
            activebackground=self.secondary_color
        )
        if width:
            btn.config(width=width)
        return btn
    
    def create_status_bar(self):
        """Create status bar"""
        status_frame = tk.Frame(self.root, bg=self.primary_color, height=40)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="✅ Ready",
            font=self.button_font,
            bg=self.primary_color,
            fg="white",
            padx=20
        )
        self.status_label.pack(side=tk.LEFT)
        
        version_label = tk.Label(
            status_frame,
            text="Advanced Translator v2.0 | 14+ Languages | Powered by Google Translate",
            font=self.small_font,
            bg=self.primary_color,
            fg="#e0e7ff",
            padx=20
        )
        version_label.pack(side=tk.RIGHT)
    
    def update_stats(self, *args):
        """Update character and word count"""
        text = self.input_text.get("1.0", tk.END).strip()
        chars = len(text)
        words = len(text.split()) if text else 0
        
        self.input_stats_label.config(
            text=f"📊 {chars} characters | {words} words"
        )
        
        output_text = self.output_text.get("1.0", tk.END).strip()
        out_chars = len(output_text)
        out_words = len(output_text.split()) if output_text else 0
        
        self.output_stats_label.config(
            text=f"📊 {out_chars} characters | {out_words} words"
        )
    
    def translate_text(self):
        """Translate input text"""
        text = self.input_text.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Empty Input", "Please enter text to translate")
            return
        
        source_lang = self.source_lang_var.get()
        if source_lang.startswith("auto"):
            src_code = "auto"
        else:
            src_code = source_lang.split(" - ")[0]
        
        dest_lang = self.dest_lang_var.get()
        dest_code = dest_lang.split(" - ")[0]
        
        self.status_label.config(text="⏳ Translating...", fg=self.warning_color)
        self.root.update()
        
        def translate_thread():
            result = self.translator.translate(text, src_lang=src_code, dest_lang=dest_code)
            self.root.after(0, lambda: self.display_translation(result, text, src_code, dest_code))
        
        thread = threading.Thread(target=translate_thread, daemon=True)
        thread.start()
    
    def display_translation(self, result, text, src_code, dest_code):
        """Display translation"""
        if result['success']:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result['translated'])
            self.output_text.config(state=tk.DISABLED)
            
            self.add_to_history(text, result['translated'], src_code, dest_code)
            self.update_stats()
            self.status_label.config(text="✅ Translation complete", fg=self.success_color)
        else:
            self.status_label.config(text=f"❌ Translation failed", fg=self.error_color)
            messagebox.showerror("Error", result['error'])
    
    def detect_language(self):
        """Detect language"""
        text = self.input_text.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Empty Input", "Please enter text")
            return
        
        try:
            result = self.translator.detect_language(text)
            
            if result['success']:
                lang = result['language']
                code = result['code']
                confidence = result['confidence']
                
                self.source_lang_var.set(f"{code} - {lang}")
                
                confidence_str = f"{confidence*100:.1f}%" if confidence else "N/A"
                msg = f"🎯 Detected Language\n\n{lang} ({code})\nConfidence: {confidence_str}"
                messagebox.showinfo("Detection", msg)
                
                self.status_label.config(text=f"✅ Detected: {lang}", fg=self.success_color)
            else:
                messagebox.showerror("Error", result['error'])
        
        except Exception as e:
            messagebox.showerror("Error", f"Detection failed: {str(e)}")
    
    def swap_languages(self):
        """Swap languages"""
        source = self.source_lang_var.get()
        dest = self.dest_lang_var.get()
        
        if source.startswith("auto"):
            messagebox.showinfo("Info", "Select a specific language first")
            return
        
        self.source_lang_var.set(dest)
        self.dest_lang_var.set(source)
        
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
            
            self.update_stats()
            self.status_label.config(text="✅ Swapped", fg=self.success_color)
    
    def add_to_history(self, original, translated, src_lang, dest_lang):
        """Add to history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item = {
            "timestamp": timestamp,
            "original": original,
            "translated": translated,
            "src_lang": src_lang,
            "dest_lang": dest_lang
        }
        
        self.history.insert(0, item)
        self.save_data()
        self.refresh_history_tree()
    
    def add_favorite(self):
        """Add favorite"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        output_text = self.output_text.get("1.0", tk.END).strip()
        
        if not input_text or not output_text:
            messagebox.showwarning("Empty", "Nothing to favorite")
            return
        
        source = self.source_lang_var.get()
        dest = self.dest_lang_var.get()
        
        favorite = {
            "original": input_text,
            "translated": output_text,
            "src_lang": source.split(" - ")[0] if "-" in source else source,
            "dest_lang": dest.split(" - ")[0]
        }
        
        self.favorites.append(favorite)
        self.save_data()
        self.refresh_favorites_tree()
        
        self.status_label.config(text="❤️ Added to favorites", fg=self.success_color)
    
    def remove_favorite(self):
        """Remove favorite"""
        selection = self.favorites_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Select favorite to remove")
            return
        
        if messagebox.askyesno("Confirm", "Remove from favorites?"):
            index = self.favorites_tree.index(selection[0])
            del self.favorites[index]
            self.save_data()
            self.refresh_favorites_tree()
    
    def clear_favorites(self):
        """Clear favorites"""
        if messagebox.askyesno("Confirm", "Clear all favorites?"):
            self.favorites = []
            self.save_data()
            self.refresh_favorites_tree()
    
    def delete_from_history(self):
        """Delete from history"""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Select item")
            return
        
        if messagebox.askyesno("Confirm", "Delete this item?"):
            index = self.history_tree.index(selection[0])
            del self.history[index]
            self.save_data()
            self.refresh_history_tree()
    
    def clear_all_history(self):
        """Clear all history"""
        if messagebox.askyesno("Confirm", "Clear all history?"):
            self.history = []
            self.save_data()
            self.refresh_history_tree()
    
    def load_from_history_tree(self, event):
        """Load from history"""
        selection = self.history_tree.selection()
        if selection:
            index = self.history_tree.index(selection[0])
            if index < len(self.history):
                item = self.history[index]
                
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", item['original'])
                
                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", item['translated'])
                self.output_text.config(state=tk.DISABLED)
                
                self.update_stats()
    
    def load_from_history(self):
        """Load from history"""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Select item")
            return
        
        self.load_from_history_tree(None)
    
    def load_from_favorites_tree(self, event):
        """Load from favorites"""
        selection = self.favorites_tree.selection()
        if selection:
            index = self.favorites_tree.index(selection[0])
            if index < len(self.favorites):
                item = self.favorites[index]
                
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", item['original'])
                
                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", item['translated'])
                self.output_text.config(state=tk.DISABLED)
                
                self.update_stats()
    
    def load_from_favorites(self):
        """Load from favorites"""
        selection = self.favorites_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Select favorite")
            return
        
        self.load_from_favorites_tree(None)
    
    def filter_history(self, *args):
        """Filter history"""
        search_term = self.history_search_var.get().lower()
        self.refresh_history_tree(search_term)
    
    def refresh_history_tree(self, search_term=""):
        """Refresh history tree"""
        self.history_tree.delete(*self.history_tree.get_children())
        
        for item in self.history:
            if not search_term or search_term in item['original'].lower() or search_term in item['translated'].lower():
                self.history_tree.insert(
                    "",
                    tk.END,
                    values=(
                        item['timestamp'],
                        f"{item['src_lang']}→{item['dest_lang']}",
                        item['original'][:55] + "..." if len(item['original']) > 55 else item['original'],
                        len(item['original'])
                    )
                )
    
    def refresh_favorites_tree(self):
        """Refresh favorites tree"""
        self.favorites_tree.delete(*self.favorites_tree.get_children())
        
        for item in self.favorites:
            self.favorites_tree.insert(
                "",
                tk.END,
                values=(
                    item['original'][:45] + "..." if len(item['original']) > 45 else item['original'],
                    item['translated'][:45] + "..." if len(item['translated']) > 45 else item['translated'],
                    f"{item['src_lang']}→{item['dest_lang']}"
                )
            )
    
    def update_statistics_display(self):
        """Update statistics"""
        total_trans = len(self.history)
        total_favs = len(self.favorites)
        
        languages_used = set()
        for item in self.history:
            languages_used.add(item['src_lang'])
            languages_used.add(item['dest_lang'])
        
        avg_length = sum(len(item['original']) for item in self.history) // max(total_trans, 1)
        
        stats_text = f"""
📊 TRANSLATION STATISTICS
{'='*60}

Total Translations: {total_trans}
Total Favorites: {total_favs}
Unique Languages Used: {len(languages_used)}
Average Text Length: {avg_length} characters

📈 LANGUAGE PAIR STATISTICS
{'-'*60}
"""
        
        lang_count = {}
        for item in self.history:
            pair = f"{item['src_lang']}→{item['dest_lang']}"
            lang_count[pair] = lang_count.get(pair, 0) + 1
        
        for pair, count in sorted(lang_count.items(), key=lambda x: x[1], reverse=True)[:10]:
            stats_text += f"\n{pair}: {count} translation(s)"
        
        stats_text += f"\n\n📅 RECENT ACTIVITY\n{'-'*60}"
        
        for i, item in enumerate(self.history[:5], 1):
            stats_text += f"\n{i}. [{item['timestamp']}]\n   {item['src_lang']}→{item['dest_lang']}: {item['original'][:50]}...\n"
        
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert("1.0", stats_text)
        self.stats_text.config(state=tk.DISABLED)
    
    def clear_input(self):
        """Clear input"""
        self.input_text.delete("1.0", tk.END)
        self.update_stats()
        self.status_label.config(text="🗑️ Input cleared", fg=self.warning_color)
    
    def copy_output(self):
        """Copy output"""
        output_text = self.output_text.get("1.0", tk.END).strip()
        if not output_text:
            messagebox.showwarning("Empty", "Nothing to copy")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(output_text)
        self.status_label.config(text="✅ Copied to clipboard", fg=self.success_color)
    
    def paste_input(self):
        """Paste input"""
        try:
            text = self.root.clipboard_get()
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", text)
            self.update_stats()
            self.status_label.config(text="✅ Pasted", fg=self.success_color)
        except Exception as e:
            messagebox.showerror("Error", f"Paste failed: {str(e)}")
    
    def export_history(self):
        """Export history"""
        if not self.history:
            messagebox.showwarning("Empty", "No history to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("All", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.history, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Success", f"Exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def toggle_theme(self):
        """Toggle theme instantly"""
        self.theme = "dark" if self.theme == "light" else "light"
        self.setup_styles()
        
        # Apply theme to root window
        self.root.configure(bg=self.bg_color)
        
        # Apply theme to header
        self.root.winfo_children()[0].configure(bg=self.primary_color)
        
        # Update theme button
        self.theme_btn.config(
            text="☀️ Light Mode" if self.theme == "dark" else "🌙 Dark Mode",
            bg="#8b7dd6"
        )
        
        # Recursively update all child widgets
        self.apply_theme_recursive(self.root)
        
        messagebox.showinfo("✅ Theme Applied", "Theme changed successfully!")
    
    def apply_theme_recursive(self, widget):
        """Recursively apply theme to all widgets"""
        try:
            # Update widget based on type
            if isinstance(widget, tk.Frame):
                widget.configure(bg=self.card_bg if 'card' in widget.winfo_name().lower() else self.bg_color)
            elif isinstance(widget, tk.Label):
                widget.configure(bg=self.card_bg if 'card' in str(widget.master).lower() else self.bg_color, fg=self.fg_color)
            elif isinstance(widget, (scrolledtext.ScrolledText, tk.Text)):
                widget.configure(
                    bg="white" if self.theme == "light" else "#3a3a52",
                    fg=self.fg_color
                )
            elif isinstance(widget, tk.Listbox):
                widget.configure(bg="white" if self.theme == "light" else "#3a3a52", fg=self.fg_color)
            
            # Recursively process children
            for child in widget.winfo_children():
                self.apply_theme_recursive(child)
        except Exception as e:
            pass  # Silently skip widgets that can't be configured
    
    def save_data(self):
        """Save data"""
        try:
            with open("translator_data.json", 'w', encoding='utf-8') as f:
                json.dump({
                    "history": self.history[:100],
                    "favorites": self.favorites[:50]
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving: {e}")
    
    def load_data(self):
        """Load data"""
        try:
            if os.path.exists("translator_data.json"):
                with open("translator_data.json", 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = data.get("history", [])
                    self.favorites = data.get("favorites", [])
            elif os.path.exists("translator_history.json"):
                with open("translator_history.json", 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"Error loading: {e}")
    
    def setup_shortcuts(self):
        """Setup shortcuts"""
        self.root.bind('<Control-Return>', lambda e: self.translate_text())
        self.root.bind('<Control-d>', lambda e: self.detect_language())
        self.root.bind('<Control-c>', lambda e: self.copy_output())


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ModernTranslatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
