import tkinter as tk
from tkinter import scrolledtext
import json
from pygments import highlight
from pygments.lexers import PythonLexer, JsonLexer
from pygments.formatters import HtmlFormatter
import autopep8

def code_formatter():
    def open_formatter_window():
        window = tk.Toplevel()
        window.title("Code Formatter")
        window.geometry("800x600")
        
        notebook = tk.ttk.Notebook(window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Python formatter tab
        python_frame = tk.Frame(notebook)
        notebook.add(python_frame, text="Python")
        
        python_text = scrolledtext.ScrolledText(python_frame, width=80, height=20)
        python_text.pack(padx=10, pady=10)
        
        def format_python():
            try:
                code = python_text.get("1.0", tk.END)
                formatted_code = autopep8.fix_code(code, options={'aggressive': 1})
                python_text.delete("1.0", tk.END)
                python_text.insert("1.0", formatted_code)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Formatting failed: {str(e)}")
        
        tk.Button(python_frame, text="Format Python Code", 
                 command=format_python).pack(pady=10)
        
        # JSON formatter tab
        json_frame = tk.Frame(notebook)
        notebook.add(json_frame, text="JSON")
        
        json_text = scrolledtext.ScrolledText(json_frame, width=80, height=20)
        json_text.pack(padx=10, pady=10)
        
        def format_json():
            try:
                text = json_text.get("1.0", tk.END).strip()
                parsed = json.loads(text)
                formatted = json.dumps(parsed, indent=4)
                json_text.delete("1.0", tk.END)
                json_text.insert("1.0", formatted)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Invalid JSON: {str(e)}")
                
        tk.Button(json_frame, text="Format JSON", 
                 command=format_json).pack(pady=10)
                
    return open_formatter_window

def json_tool():
    def open_json_tool():
        window = tk.Toplevel()
        window.title("JSON Tool")
        window.geometry("800x600")
        
        # Input
        input_frame = tk.LabelFrame(window, text="Input JSON")
        input_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        input_text = scrolledtext.ScrolledText(input_frame, height=10)
        input_text.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Output
        output_frame = tk.LabelFrame(window, text="Output")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        output_text = scrolledtext.ScrolledText(output_frame, height=10)
        output_text.pack(padx=5, pady=5, fill="both", expand=True)
        
        def validate_json():
            try:
                text = input_text.get("1.0", tk.END).strip()
                parsed = json.loads(text)
                output_text.delete("1.0", tk.END)
                output_text.insert("1.0", "✓ Valid JSON")
                return parsed
            except Exception as e:
                output_text.delete("1.0", tk.END)
                output_text.insert("1.0", f"❌ Invalid JSON: {str(e)}")
                return None
        
        def minify():
            parsed = validate_json()
            if parsed:
                minified = json.dumps(parsed, separators=(',', ':'))
                output_text.delete("1.0", tk.END)
                output_text.insert("1.0", minified)
        
        def prettify():
            parsed = validate_json()
            if parsed:
                pretty = json.dumps(parsed, indent=4)
                output_text.delete("1.0", tk.END)
                output_text.insert("1.0", pretty)
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Validate", command=validate_json).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Minify", command=minify).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Prettify", command=prettify).pack(side="left", padx=5)
    
    return open_json_tool

def get_tools():
    return [
        {
            "name": "Code Formatter",
            "description": "Format and beautify Python code and JSON",
            "callback": code_formatter()
        },
        {
            "name": "JSON Tool",
            "description": "Validate, format, minify and analyze JSON data",
            "callback": json_tool()
        }
    ]
