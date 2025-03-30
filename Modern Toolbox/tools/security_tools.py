import customtkinter as ctk
import string
import random
import hashlib
import base64

def password_generator():
    def open_generator():
        window = ctk.CTkToplevel()
        window.title("Password Generator")
        window.geometry("400x500")

        options_frame = ctk.CTkFrame(window)
        options_frame.pack(padx=10, pady=10, fill="x")

        # Password options
        length_var = ctk.IntVar(value=12)
        length_label = ctk.CTkLabel(options_frame, text="Length:")
        length_label.pack(pady=5)
        length_slider = ctk.CTkSlider(options_frame, from_=8, to=32, 
                                    variable=length_var)
        length_slider.pack(pady=5)
        
        # Checkboxes for character types
        uppercase_var = ctk.BooleanVar(value=True)
        lowercase_var = ctk.BooleanVar(value=True)
        numbers_var = ctk.BooleanVar(value=True)
        symbols_var = ctk.BooleanVar(value=True)
        
        ctk.CTkCheckBox(options_frame, text="Uppercase (A-Z)", 
                       variable=uppercase_var).pack(pady=5)
        ctk.CTkCheckBox(options_frame, text="Lowercase (a-z)", 
                       variable=lowercase_var).pack(pady=5)
        ctk.CTkCheckBox(options_frame, text="Numbers (0-9)", 
                       variable=numbers_var).pack(pady=5)
        ctk.CTkCheckBox(options_frame, text="Symbols (!@#$%^&*)", 
                       variable=symbols_var).pack(pady=5)

        # Result display
        result_var = ctk.StringVar()
        result_entry = ctk.CTkEntry(window, textvariable=result_var, 
                                  width=300, height=40)
        result_entry.pack(pady=20)

        def generate_password():
            chars = ""
            if uppercase_var.get():
                chars += string.ascii_uppercase
            if lowercase_var.get():
                chars += string.ascii_lowercase
            if numbers_var.get():
                chars += string.digits
            if symbols_var.get():
                chars += string.punctuation
                
            if not chars:
                result_var.set("Please select at least one character type")
                return
                
            password = ''.join(random.choice(chars) for _ in range(length_var.get()))
            result_var.set(password)

        def copy_to_clipboard():
            window.clipboard_clear()
            window.clipboard_append(result_var.get())

        ctk.CTkButton(window, text="Generate Password", 
                     command=generate_password).pack(pady=10)
        ctk.CTkButton(window, text="Copy to Clipboard", 
                     command=copy_to_clipboard).pack(pady=5)

    return open_generator

def hash_calculator():
    def open_hash_calc():
        window = ctk.CTkToplevel()
        window.title("Hash Calculator")
        window.geometry("500x400")
        
        input_text = ctk.CTkTextbox(window, height=100)
        input_text.pack(padx=10, pady=10, fill="x")
        
        result_frame = ctk.CTkFrame(window)
        result_frame.pack(padx=10, pady=10, fill="x")
        
        hash_results = {}
        for algorithm in ['md5', 'sha1', 'sha256', 'sha512']:
            var = ctk.StringVar()
            hash_results[algorithm] = var
            label = ctk.CTkLabel(result_frame, text=f"{algorithm.upper()}:")
            label.pack(pady=2)
            entry = ctk.CTkEntry(result_frame, textvariable=var, width=300)
            entry.pack(pady=2)
        
        def calculate_hashes():
            text = input_text.get("1.0", "end-1c").encode('utf-8')
            for algorithm in hash_results:
                hasher = hashlib.new(algorithm)
                hasher.update(text)
                hash_results[algorithm].set(hasher.hexdigest())
        
        ctk.CTkButton(window, text="Calculate Hashes", 
                     command=calculate_hashes).pack(pady=10)
    
    return open_hash_calc

def text_encoder():
    def open_encoder():
        window = ctk.CTkToplevel()
        window.title("Text Encoder/Decoder")
        window.geometry("500x600")
        
        input_frame = ctk.CTkFrame(window)
        input_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(input_frame, text="Input Text:").pack()
        input_text = ctk.CTkTextbox(input_frame, height=100)
        input_text.pack(padx=10, pady=5, fill="x")
        
        output_frame = ctk.CTkFrame(window)
        output_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(output_frame, text="Output:").pack()
        output_text = ctk.CTkTextbox(output_frame, height=100)
        output_text.pack(padx=10, pady=5, fill="x")
        
        def encode_base64():
            text = input_text.get("1.0", "end-1c").encode('utf-8')
            encoded = base64.b64encode(text).decode('utf-8')
            output_text.delete("1.0", "end")
            output_text.insert("1.0", encoded)
            
        def decode_base64():
            try:
                text = input_text.get("1.0", "end-1c")
                decoded = base64.b64decode(text).decode('utf-8')
                output_text.delete("1.0", "end")
                output_text.insert("1.0", decoded)
            except:
                output_text.delete("1.0", "end")
                output_text.insert("1.0", "Invalid Base64 input")
                
        buttons_frame = ctk.CTkFrame(window)
        buttons_frame.pack(pady=10)
        
        ctk.CTkButton(buttons_frame, text="Encode Base64", 
                     command=encode_base64).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Decode Base64", 
                     command=decode_base64).pack(side="left", padx=5)
    
    return open_encoder

def get_tools():
    return [
        {
            "name": "Password Generator",
            "description": "Generate secure passwords with customizable options",
            "callback": password_generator()
        },
        {
            "name": "Hash Calculator",
            "description": "Calculate MD5, SHA1, SHA256, and SHA512 hashes",
            "callback": hash_calculator()
        },
        {
            "name": "Text Encoder/Decoder",
            "description": "Encode/decode text using Base64",
            "callback": text_encoder()
        }
    ]