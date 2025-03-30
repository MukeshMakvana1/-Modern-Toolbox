from PIL import Image, ImageEnhance, ImageFilter
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path

def image_resizer():
    def open_resize_window():
        window = tk.Toplevel()
        window.title("Image Resizer")
        window.geometry("400x500")
        
        # File selection
        file_frame = tk.LabelFrame(window, text="Image Selection")
        file_frame.pack(fill="x", padx=10, pady=5)
        
        file_path_var = tk.StringVar()
        tk.Label(file_frame, textvariable=file_path_var, wraplength=350).pack(pady=5)
        
        # Size options
        options_frame = tk.LabelFrame(window, text="Resize Options")
        options_frame.pack(fill="x", padx=10, pady=5)
        
        # Width and height entries
        size_frame = tk.Frame(options_frame)
        size_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(size_frame, text="Width:").pack(side="left", padx=5)
        width_var = tk.StringVar()
        width_entry = tk.Entry(size_frame, textvariable=width_var, width=10)
        width_entry.pack(side="left", padx=5)
        
        tk.Label(size_frame, text="Height:").pack(side="left", padx=5)
        height_var = tk.StringVar()
        height_entry = tk.Entry(size_frame, textvariable=height_var, width=10)
        height_entry.pack(side="left", padx=5)
        
        # Maintain aspect ratio
        aspect_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Maintain aspect ratio", 
                      variable=aspect_var).pack(pady=5)
        
        # Preview
        preview_frame = tk.LabelFrame(window, text="Preview")
        preview_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        preview_label = tk.Label(preview_frame)
        preview_label.pack(pady=5)
        
        def select_image():
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )
            if file_path:
                file_path_var.set(file_path)
                img = Image.open(file_path)
                width_var.set(str(img.width))
                height_var.set(str(img.height))
                update_preview()
        
        def update_preview():
            try:
                if not file_path_var.get():
                    return
                    
                img = Image.open(file_path_var.get())
                width = int(width_var.get())
                height = int(height_var.get())
                
                if aspect_var.get():
                    ratio = min(width/img.width, height/img.height)
                    width = int(img.width * ratio)
                    height = int(img.height * ratio)
                
                preview = img.copy()
                preview.thumbnail((200, 200))  # Preview size
                preview = preview.resize((preview.width, preview.height))
                preview.tk = preview  # Prevent garbage collection
                preview_label.configure(image=preview)
                
            except Exception as e:
                tk.messagebox.showerror("Error", str(e))
        
        def save_image():
            try:
                if not file_path_var.get():
                    return
                    
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), 
                              ("JPEG files", "*.jpg"),
                              ("All files", "*.*")]
                )
                
                if save_path:
                    img = Image.open(file_path_var.get())
                    width = int(width_var.get())
                    height = int(height_var.get())
                    
                    if aspect_var.get():
                        ratio = min(width/img.width, height/img.height)
                        width = int(img.width * ratio)
                        height = int(img.height * ratio)
                    
                    resized = img.resize((width, height), Image.Resampling.LANCZOS)
                    resized.save(save_path)
                    tk.messagebox.showinfo("Success", "Image saved successfully!")
                    
            except Exception as e:
                tk.messagebox.showerror("Error", str(e))
        
        # Buttons
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Select Image", 
                 command=select_image).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update Preview", 
                 command=update_preview).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Save Image", 
                 command=save_image).pack(side="left", padx=5)

    return open_resize_window

def image_editor():
    def open_editor():
        window = tk.Toplevel()
        window.title("Image Editor")
        window.geometry("800x600")
        
        # File selection
        file_frame = tk.LabelFrame(window, text="Image Selection")
        file_frame.pack(fill="x", padx=10, pady=5)
        
        file_path_var = tk.StringVar()
        tk.Label(file_frame, textvariable=file_path_var, wraplength=750).pack(pady=5)
        
        # Image display
        canvas_frame = tk.LabelFrame(window, text="Image")
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        image_label = tk.Label(canvas_frame)
        image_label.pack(pady=5)
        
        # Editing tools
        tools_frame = tk.LabelFrame(window, text="Tools")
        tools_frame.pack(fill="x", padx=10, pady=5)
        
        # Sliders for adjustments
        def make_slider(text, from_, to, default):
            frame = tk.Frame(tools_frame)
            frame.pack(fill="x", padx=5, pady=2)
            tk.Label(frame, text=text, width=10).pack(side="left")
            var = tk.DoubleVar(value=default)
            slider = ttk.Scale(frame, from_=from_, to=to, 
                             variable=var, orient="horizontal")
            slider.pack(side="left", fill="x", expand=True, padx=5)
            return var
        
        brightness_var = make_slider("Brightness", 0.0, 2.0, 1.0)
        contrast_var = make_slider("Contrast", 0.0, 2.0, 1.0)
        saturation_var = make_slider("Saturation", 0.0, 2.0, 1.0)
        sharpness_var = make_slider("Sharpness", 0.0, 2.0, 1.0)
        
        # Image operations
        current_image = None
        original_image = None
        
        def select_image():
            nonlocal current_image, original_image
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )
            if file_path:
                file_path_var.set(file_path)
                original_image = Image.open(file_path)
                current_image = original_image.copy()
                update_preview()
        
        def update_preview():
            if current_image is None:
                return
                
            # Apply adjustments
            img = original_image.copy()
            
            # Brightness
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness_var.get())
            
            # Contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_var.get())
            
            # Color/Saturation
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(saturation_var.get())
            
            # Sharpness
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(sharpness_var.get())
            
            # Update preview
            preview = img.copy()
            preview.thumbnail((600, 400))  # Preview size
            preview.tk = preview  # Prevent garbage collection
            image_label.configure(image=preview)
            current_image = img
        
        def apply_filter(filter_type):
            if current_image is None:
                return
                
            try:
                if filter_type == "blur":
                    current_image = current_image.filter(ImageFilter.BLUR)
                elif filter_type == "sharpen":
                    current_image = current_image.filter(ImageFilter.SHARPEN)
                elif filter_type == "edge":
                    current_image = current_image.filter(ImageFilter.FIND_EDGES)
                elif filter_type == "emboss":
                    current_image = current_image.filter(ImageFilter.EMBOSS)
                update_preview()
            except Exception as e:
                tk.messagebox.showerror("Error", str(e))
        
        def save_image():
            if current_image is None:
                return
                
            try:
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), 
                              ("JPEG files", "*.jpg"),
                              ("All files", "*.*")]
                )
                if save_path:
                    current_image.save(save_path)
                    tk.messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                tk.messagebox.showerror("Error", str(e))
        
        # Control buttons
        btn_frame = tk.Frame(tools_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Select Image", 
                 command=select_image).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update Preview", 
                 command=update_preview).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Blur", 
                 command=lambda: apply_filter("blur")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Sharpen", 
                 command=lambda: apply_filter("sharpen")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Find Edges", 
                 command=lambda: apply_filter("edge")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Emboss", 
                 command=lambda: apply_filter("emboss")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Save Image", 
                 command=save_image).pack(side="left", padx=5)
        
        # Bind slider updates
        for var in [brightness_var, contrast_var, saturation_var, sharpness_var]:
            var.trace_add("write", lambda *args: update_preview())

    return open_editor

def get_tools():
    return [
        {
            "name": "Image Resizer",
            "description": "Resize images with preview and aspect ratio control",
            "callback": image_resizer()
        },
        {
            "name": "Image Editor",
            "description": "Edit images with filters and adjustments",
            "callback": image_editor()
        }
    ]
