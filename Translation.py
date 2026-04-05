# ========================================================
# SMART TRANSLATOR PRO - GUI Translation System
# ========================================================
# Requirements:
# 1. pip install googletrans==4.0.0-rc1
# 2. Internet connection required for translation (uses Google Translate)
# 3. Python 3.8+ and Tkinter (usually pre-installed)
#
# Features:
# - Beautiful modern GUI with ttk theme and custom colors
# - Language selection (Auto Detect supported for source)
# - Swap languages button with emoji
# - Input + Output with ScrolledText
# - Full translation history stored in SQLite3 database
# - Scrollable Treeview history with vertical scrollbar
# - Preview of long texts in history + Double-click for full view
# - Delete selected entry or Clear ALL history
# - Attractive dark/light professional look with emojis and styling
# - Error handling and user-friendly messages
#
# Database file: translation_history.db (created automatically in the same folder)
# ========================================================

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import sqlite3
from datetime import datetime
from googletrans import Translator, LANGUAGES


class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 Smart Translator Pro")
        self.root.geometry("1350x820")
        self.root.configure(bg="#2C3E50")
        self.root.minsize(1200, 700)

        # Initialize translator and language mappings
        self.translator = Translator()
        self.supported_languages = {name.capitalize(): code for code, name in LANGUAGES.items()}
        self.history_data = {}  # id -> (original_full, translated_full) for quick full view

        self.init_database()
        self.create_widgets()
        self.load_history()

    def init_database(self):
        """Create SQLite database and table if not exists"""
        conn = sqlite3.connect("translation_history.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source_lang TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                original TEXT NOT NULL,
                translated TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def create_widgets(self):
        """Build the beautiful GUI"""
        style = ttk.Style()
        style.theme_use("clam")

        # Custom styling for attractive modern look
        style.configure("TFrame", background="#ECF0F1")
        style.configure("TLabel", background="#ECF0F1", foreground="#2C3E50", font=("Helvetica", 11))
        style.configure("TButton", background="#3498DB", foreground="white", font=("Helvetica", 11, "bold"), padding=8)
        style.map("TButton", background=[("active", "#2980B9")])
        style.configure("Treeview", background="#F8F9FA", fieldbackground="#F8F9FA", foreground="#2C3E50", font=("Helvetica", 10))
        style.configure("Treeview.Heading", background="#3498DB", foreground="white", font=("Helvetica", 11, "bold"))
        style.configure("TLabelframe", background="#ECF0F1", foreground="#2C3E50", font=("Helvetica", 12, "bold"))

        # Main container
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ===================== LEFT PANEL - TRANSLATION =====================
        left_frame = ttk.Frame(main_frame, width=780)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        left_frame.pack_propagate(False)

        # Header
        header = tk.Label(
            left_frame,
            text="🌍 Translate Any Text Instantly",
            font=("Helvetica", 22, "bold"),
            bg="#ECF0F1",
            fg="#2980B9"
        )
        header.pack(pady=(0, 15))

        # Language selection bar
        lang_bar = ttk.Frame(left_frame)
        lang_bar.pack(fill=tk.X, pady=8)

        ttk.Label(lang_bar, text="From:", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=(5, 8))
        source_langs = ["Auto Detect"] + sorted(self.supported_languages.keys())
        self.combo_source = ttk.Combobox(lang_bar, values=source_langs, state="readonly", width=22, font=("Helvetica", 11))
        self.combo_source.pack(side=tk.LEFT, padx=5)
        self.combo_source.set("Auto Detect")

        # Swap button
        self.swap_btn = ttk.Button(
            lang_bar,
            text="🔄 Swap Languages",
            command=self.swap_languages,
            width=18
        )
        self.swap_btn.pack(side=tk.LEFT, padx=12)

        ttk.Label(lang_bar, text="To:", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=(5, 8))
        target_langs = sorted(self.supported_languages.keys())
        self.combo_target = ttk.Combobox(lang_bar, values=target_langs, state="readonly", width=22, font=("Helvetica", 11))
        self.combo_target.pack(side=tk.LEFT, padx=5)
        self.combo_target.set("English")

        # Input section
        input_label_frame = ttk.LabelFrame(left_frame, text=" 📝 Input Text ", padding=12)
        input_label_frame.pack(fill=tk.BOTH, expand=True, pady=12)

        self.input_text = ScrolledText(
            input_label_frame,
            height=11,
            font=("Helvetica", 12),
            wrap=tk.WORD,
            bg="#F8F9FA",
            fg="#2C3E50",
            relief="flat",
            borderwidth=0
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)

        # Action buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(pady=12)

        self.translate_btn = ttk.Button(
            btn_frame,
            text="🔄 TRANSLATE NOW",
            command=self.translate_text,
            style="TButton"
        )
        self.translate_btn.pack(side=tk.LEFT, padx=8)

        ttk.Button(
            btn_frame,
            text="🗑 Clear Input",
            command=self.clear_input
        ).pack(side=tk.LEFT, padx=8)

        # Output section
        output_label_frame = ttk.LabelFrame(left_frame, text=" ✅ Translated Text ", padding=12)
        output_label_frame.pack(fill=tk.BOTH, expand=True, pady=12)

        self.output_text = ScrolledText(
            output_label_frame,
            height=11,
            font=("Helvetica", 12),
            wrap=tk.WORD,
            bg="#F8F9FA",
            fg="#27AE60",
            relief="flat",
            borderwidth=0
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.output_text.configure(state="disabled")

        # ===================== RIGHT PANEL - HISTORY =====================
        right_frame = ttk.Frame(main_frame, width=520)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        right_frame.pack_propagate(False)

        hist_header = tk.Label(
            right_frame,
            text="📜 Translation History",
            font=("Helvetica", 18, "bold"),
            bg="#ECF0F1",
            fg="#2980B9"
        )
        hist_header.pack(pady=(0, 10))

        # Treeview + Scrollbar container
        tree_container = ttk.Frame(right_frame)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=5)

        self.tree = ttk.Treeview(
            tree_container,
            columns=("id", "timestamp", "langs", "original", "translated"),
            show="headings",
            height=22
        )

        # Headings
        self.tree.heading("id", text="ID")
        self.tree.heading("timestamp", text="🕒 Time")
        self.tree.heading("langs", text="Languages")
        self.tree.heading("original", text="Original (preview)")
        self.tree.heading("translated", text="Translated (preview)")

        # Column widths for clean look
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("timestamp", width=130)
        self.tree.column("langs", width=110)
        self.tree.column("original", width=190)
        self.tree.column("translated", width=190)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical scrollbar for history
        v_scroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=v_scroll.set)

        # History action buttons
        hist_btn_frame = ttk.Frame(right_frame)
        hist_btn_frame.pack(pady=12, fill=tk.X)

        ttk.Button(
            hist_btn_frame,
            text="🗑 Delete Selected",
            command=self.delete_selected
        ).pack(side=tk.LEFT, padx=6)

        ttk.Button(
            hist_btn_frame,
            text="🧹 Clear All History",
            command=self.clear_all_history
        ).pack(side=tk.LEFT, padx=6)

        # Double-click to view full translation
        self.tree.bind("<Double-1>", self.show_full_translation)

        # Footer
        footer = tk.Label(
            self.root,
            text="💡 Powered by Google Translate • History saved securely in SQLite3 • Scroll to browse past translations",
            bg="#2C3E50",
            fg="#ECF0F1",
            font=("Helvetica", 9)
        )
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=8)

    def swap_languages(self):
        """Swap source and target languages"""
        source = self.combo_source.get()
        target = self.combo_target.get()

        if source == "Auto Detect":
            messagebox.showinfo("Swap Info", "Cannot swap when source is 'Auto Detect'.\nPlease select a specific source language first.")
            return

        self.combo_source.set(target)
        self.combo_target.set(source)

    def clear_input(self):
        """Clear input text area"""
        self.input_text.delete("1.0", tk.END)

    def translate_text(self):
        """Perform translation and save to history"""
        input_str = self.input_text.get("1.0", tk.END).strip()
        if not input_str:
            messagebox.showwarning("Empty Input", "Please enter some text to translate!")
            return

        source_name = self.combo_source.get()
        target_name = self.combo_target.get()

        if not target_name:
            messagebox.showwarning("Language Required", "Please select a target language.")
            return

        # Determine source code
        if source_name == "Auto Detect":
            src_code = "auto"
        else:
            src_code = self.supported_languages.get(source_name)

        tgt_code = self.supported_languages.get(target_name)

        try:
            result = self.translator.translate(input_str, src=src_code, dest=tgt_code)
            translated_text = result.text

            # Show in output area
            self.output_text.configure(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated_text)
            self.output_text.configure(state="disabled")

            # Save to database
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = sqlite3.connect("translation_history.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO history 
                (timestamp, source_lang, target_lang, original, translated)
                VALUES (?, ?, ?, ?, ?)
            """, (timestamp, source_name, target_name, input_str, translated_text))
            conn.commit()
            conn.close()

            # Refresh history
            self.load_history()

            # Success feedback
            self.root.title("🌐 Smart Translator Pro ✓ Translation Successful!")

        except Exception as e:
            messagebox.showerror(
                "Translation Failed",
                f"Could not translate the text.\n\nError: {str(e)}\n\nPlease check your internet connection."
            )

    def load_history(self):
        """Load all history into Treeview with previews"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.history_data.clear()

        conn = sqlite3.connect("translation_history.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            hid, timestamp, src, tgt, orig, trans = row

            # Create nice previews
            orig_preview = (orig[:48] + "…") if len(orig) > 48 else orig
            trans_preview = (trans[:48] + "…") if len(trans) > 48 else trans

            self.tree.insert(
                "",
                tk.END,
                values=(hid, timestamp, f"{src} → {tgt}", orig_preview, trans_preview)
            )
            self.history_data[hid] = (orig, trans)

    def delete_selected(self):
        """Delete selected history item"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Nothing Selected", "Please select a history entry to delete.")
            return

        if messagebox.askyesno("Confirm Delete", "Delete this translation from history permanently?"):
            item = self.tree.item(selected_items[0])
            hid = item["values"][0]

            conn = sqlite3.connect("translation_history.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history WHERE id = ?", (hid,))
            conn.commit()
            conn.close()

            if hid in self.history_data:
                del self.history_data[hid]

            self.load_history()

    def clear_all_history(self):
        """Clear entire history with confirmation"""
        if messagebox.askyesno(
            "⚠️ Clear All History",
            "This will permanently delete ALL translation records.\n\nAre you absolutely sure?",
            icon="warning"
        ):
            conn = sqlite3.connect("translation_history.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history")
            conn.commit()
            conn.close()

            self.history_data.clear()
            self.load_history()
            messagebox.showinfo("History Cleared", "All translation history has been removed.")

    def show_full_translation(self, event):
        """Show full original + translated text in a popup when double-clicked"""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = self.tree.item(selected_items[0])
        hid = item["values"][0]

        if hid in self.history_data:
            orig_full, trans_full = self.history_data[hid]
            display_text = f"""🕒 Timestamp: {item['values'][1]}
🔠 Languages: {item['values'][2]}

📝 ORIGINAL TEXT:
{orig_full}

────────────────────────────────────
🔄 TRANSLATED TEXT:
{trans_full}
"""
            messagebox.showinfo("Full Translation Record", display_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
