"""
Text utility functions for the Image Resizer App
"""

import customtkinter as ctk
from tkinter import scrolledtext
import string

def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to max_length and add ellipsis if necessary"""
    return text if len(text) <= max_length else f"{text[:max_length-3]}..."

def format_size(size_bytes: int) -> str:
    """Convert bytes to human readable string"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def text_case_converter():
    def open_converter():
        window = ctk.CTkToplevel()
        window.title("Text Case Converter")
        window.geometry("500x400")
        
        text_area = scrolledtext.ScrolledText(window, width=50, height=10)
        text_area.pack(padx=10, pady=10)
        
        buttons_frame = ctk.CTkFrame(window)
        buttons_frame.pack(pady=10)
        
        def convert_case(case_type):
            text = text_area.get("1.0", "end-1c")
            if case_type == "upper":
                result = text.upper()
            elif case_type == "lower":
                result = text.lower()
            elif case_type == "title":
                result = string.capwords(text)
            elif case_type == "sentence":
                result = text.capitalize()
            
            text_area.delete("1.0", "end")
            text_area.insert("1.0", result)
        
        ctk.CTkButton(buttons_frame, text="UPPERCASE", 
                     command=lambda: convert_case("upper")).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="lowercase", 
                     command=lambda: convert_case("lower")).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Title Case", 
                     command=lambda: convert_case("title")).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Sentence case", 
                     command=lambda: convert_case("sentence")).pack(side="left", padx=5)
    
    return open_converter

def text_counter():
    def open_counter():
        window = ctk.CTkToplevel()
        window.title("Text Counter")
        window.geometry("500x400")
        
        text_area = scrolledtext.ScrolledText(window, width=50, height=10)
        text_area.pack(padx=10, pady=10)
        
        stats_frame = ctk.CTkFrame(window)
        stats_frame.pack(pady=10, fill="x", padx=10)
        
        chars_label = ctk.CTkLabel(stats_frame, text="Characters: 0")
        chars_label.pack(pady=5)
        
        words_label = ctk.CTkLabel(stats_frame, text="Words: 0")
        words_label.pack(pady=5)
        
        lines_label = ctk.CTkLabel(stats_frame, text="Lines: 0")
        lines_label.pack(pady=5)
        
        def update_stats(event=None):
            text = text_area.get("1.0", "end-1c")
            chars = len(text)
            words = len(text.split())
            lines = len(text.splitlines()) or 1
            
            chars_label.configure(text=f"Characters: {chars}")
            words_label.configure(text=f"Words: {words}")
            lines_label.configure(text=f"Lines: {lines}")
        
        text_area.bind("<KeyRelease>", update_stats)
    
    return open_counter

def text_formatter():
    def open_formatter():
        window = ctk.CTkToplevel()
        window.title("Text Formatter")
        window.geometry("500x400")
        
        text_area = scrolledtext.ScrolledText(window, width=50, height=10)
        text_area.pack(padx=10, pady=10)
        
        def remove_extra_spaces():
            text = text_area.get("1.0", "end-1c")
            # Remove multiple spaces
            formatted = " ".join(text.split())
            text_area.delete("1.0", "end")
            text_area.insert("1.0", formatted)
            
        def remove_empty_lines():
            text = text_area.get("1.0", "end-1c")
            # Remove empty lines while preserving paragraph structure
            formatted = "\n".join(line.strip() for line in text.splitlines() if line.strip())
            text_area.delete("1.0", "end")
            text_area.insert("1.0", formatted)
        
        buttons_frame = ctk.CTkFrame(window)
        buttons_frame.pack(pady=10)
        
        ctk.CTkButton(buttons_frame, text="Remove Extra Spaces", 
                     command=remove_extra_spaces).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Remove Empty Lines", 
                     command=remove_empty_lines).pack(side="left", padx=5)
    
    return open_formatter

def get_tools():
    return [
        {
            "name": "Text Case Converter",
            "description": "Convert text between different cases (upper, lower, title, sentence)",
            "callback": text_case_converter()
        },
        {
            "name": "Text Counter",
            "description": "Count characters, words, and lines in text",
            "callback": text_counter()
        },
        {
            "name": "Text Formatter",
            "description": "Clean and format text (remove extra spaces, empty lines)",
            "callback": text_formatter()
        }
    ]
