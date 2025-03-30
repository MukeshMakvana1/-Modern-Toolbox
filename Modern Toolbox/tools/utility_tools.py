import customtkinter as ctk
import tkinter as tk
from tkinter import colorchooser
import math
import time
from datetime import datetime, timedelta

def calculator():
    def open_calculator():
        window = ctk.CTkToplevel()
        window.title("Calculator")
        window.geometry("300x400")
        
        # Display
        display_var = ctk.StringVar(value="0")
        display = ctk.CTkEntry(window, textvariable=display_var, 
                             width=280, height=50, justify="right")
        display.pack(padx=10, pady=10)
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(window)
        btn_frame.pack(padx=10, pady=5)
        
        current = []
        
        def button_click(value):
            if value == "=":
                try:
                    result = eval("".join(current))
                    display_var.set(result)
                    current.clear()
                    current.append(str(result))
                except:
                    display_var.set("Error")
                    current.clear()
            elif value == "C":
                current.clear()
                display_var.set("0")
            elif value == "⌫":
                if current:
                    current.pop()
                    display_var.set("".join(current) if current else "0")
            else:
                current.append(value)
                display_var.set("".join(current))
        
        # Calculator buttons
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["(", ")", "C", "⌫"]
        ]
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                btn = ctk.CTkButton(btn_frame, text=text, width=60, height=40,
                                  command=lambda t=text: button_click(t))
                btn.grid(row=i, column=j, padx=2, pady=2)
        
        # Scientific functions
        sci_frame = ctk.CTkFrame(window)
        sci_frame.pack(padx=10, pady=5)
        
        sci_functions = [
            ("sin", lambda x: str(math.sin(math.radians(float(x))))),
            ("cos", lambda x: str(math.cos(math.radians(float(x))))),
            ("tan", lambda x: str(math.tan(math.radians(float(x))))),
            ("√", lambda x: str(math.sqrt(float(x)))),
            ("x²", lambda x: str(float(x) ** 2))
        ]
        
        def apply_sci_func(func):
            try:
                result = func("".join(current))
                current.clear()
                current.append(result)
                display_var.set(result)
            except:
                display_var.set("Error")
                current.clear()
        
        for i, (text, func) in enumerate(sci_functions):
            btn = ctk.CTkButton(sci_frame, text=text, width=50, height=30,
                              command=lambda f=func: apply_sci_func(f))
            btn.grid(row=0, column=i, padx=2, pady=2)
            
    return open_calculator

def unit_converter():
    def open_converter():
        window = ctk.CTkToplevel()
        window.title("Unit Converter")
        window.geometry("400x500")
        
        # Unit conversion definitions
        conversions = {
            "Length": {
                "m": 1,
                "km": 1000,
                "cm": 0.01,
                "mm": 0.001,
                "in": 0.0254,
                "ft": 0.3048,
                "yd": 0.9144,
                "mi": 1609.34
            },
            "Weight": {
                "kg": 1,
                "g": 0.001,
                "mg": 0.000001,
                "lb": 0.453592,
                "oz": 0.0283495
            },
            "Temperature": {
                "°C": "C",
                "°F": "F",
                "K": "K"
            }
        }
        
        # Category selection
        category_var = ctk.StringVar(value="Length")
        category_frame = ctk.CTkFrame(window)
        category_frame.pack(padx=10, pady=5, fill="x")
        
        for cat in conversions.keys():
            ctk.CTkRadioButton(category_frame, text=cat, variable=category_var,
                             value=cat, command=lambda: update_units()).pack(side="left", padx=10)
        
        # Conversion inputs
        input_frame = ctk.CTkFrame(window)
        input_frame.pack(padx=10, pady=5, fill="x")
        
        from_unit_var = ctk.StringVar()
        to_unit_var = ctk.StringVar()
        
        # From section
        from_frame = ctk.CTkFrame(input_frame)
        from_frame.pack(side="left", padx=5, fill="x", expand=True)
        
        from_value = ctk.CTkEntry(from_frame, width=120)
        from_value.pack(pady=5)
        
        from_unit = ctk.CTkOptionMenu(from_frame, variable=from_unit_var)
        from_unit.pack(pady=5)
        
        # To section
        to_frame = ctk.CTkFrame(input_frame)
        to_frame.pack(side="right", padx=5, fill="x", expand=True)
        
        to_value = ctk.CTkEntry(to_frame, width=120)
        to_value.pack(pady=5)
        
        to_unit = ctk.CTkOptionMenu(to_frame, variable=to_unit_var)
        to_unit.pack(pady=5)
        
        def update_units():
            category = category_var.get()
            units = list(conversions[category].keys())
            
            from_unit.configure(values=units)
            to_unit.configure(values=units)
            
            if not from_unit_var.get() in units:
                from_unit_var.set(units[0])
            if not to_unit_var.get() in units:
                to_unit_var.set(units[0])
        
        def convert():
            try:
                value = float(from_value.get())
                from_u = from_unit_var.get()
                to_u = to_unit_var.get()
                category = category_var.get()
                
                if category == "Temperature":
                    # Special handling for temperature
                    if from_u == "°C":
                        if to_u == "°F":
                            result = value * 9/5 + 32
                        elif to_u == "K":
                            result = value + 273.15
                        else:
                            result = value
                    elif from_u == "°F":
                        if to_u == "°C":
                            result = (value - 32) * 5/9
                        elif to_u == "K":
                            result = (value - 32) * 5/9 + 273.15
                        else:
                            result = value
                    else:  # Kelvin
                        if to_u == "°C":
                            result = value - 273.15
                        elif to_u == "°F":
                            result = (value - 273.15) * 9/5 + 32
                        else:
                            result = value
                else:
                    # Standard conversion through base unit
                    base_value = value * conversions[category][from_u]
                    result = base_value / conversions[category][to_u]
                
                to_value.delete(0, tk.END)
                to_value.insert(0, f"{result:.6g}")
                
            except ValueError:
                to_value.delete(0, tk.END)
                to_value.insert(0, "Invalid input")
        
        # Convert button
        ctk.CTkButton(window, text="Convert", 
                     command=convert).pack(pady=10)
        
        # Initialize units
        update_units()
    
    return open_converter

def color_picker():
    def open_picker():
        window = ctk.CTkToplevel()
        window.title("Color Picker")
        window.geometry("400x500")
        
        # Color display
        color_frame = ctk.CTkFrame(window, width=200, height=100)
        color_frame.pack(padx=10, pady=10)
        
        # Color values
        values_frame = ctk.CTkFrame(window)
        values_frame.pack(padx=10, pady=5, fill="x")
        
        hex_var = ctk.StringVar()
        rgb_var = ctk.StringVar()
        hsv_var = ctk.StringVar()
        
        def create_value_display(text, variable):
            frame = ctk.CTkFrame(values_frame)
            frame.pack(fill="x", pady=2)
            ctk.CTkLabel(frame, text=text).pack(side="left", padx=5)
            entry = ctk.CTkEntry(frame, textvariable=variable, width=200)
            entry.pack(side="right", padx=5)
            return entry
        
        hex_entry = create_value_display("Hex:", hex_var)
        rgb_entry = create_value_display("RGB:", rgb_var)
        hsv_entry = create_value_display("HSV:", hsv_var)
        
        def update_color_values(color):
            # Update hex
            hex_value = '#{:02x}{:02x}{:02x}'.format(*[int(x) for x in color])
            hex_var.set(hex_value)
            
            # Update RGB
            rgb_value = f"rgb({int(color[0])}, {int(color[1])}, {int(color[2])})"
            rgb_var.set(rgb_value)
            
            # Convert to HSV
            r, g, b = [x/255 for x in color]
            cmax = max(r, g, b)
            cmin = min(r, g, b)
            diff = cmax - cmin
            
            if cmax == cmin:
                h = 0
            elif cmax == r:
                h = (60 * ((g-b)/diff) + 360) % 360
            elif cmax == g:
                h = (60 * ((b-r)/diff) + 120) % 360
            else:
                h = (60 * ((r-g)/diff) + 240) % 360
            
            s = 0 if cmax == 0 else (diff / cmax) * 100
            v = cmax * 100
            
            hsv_value = f"hsv({int(h)}°, {int(s)}%, {int(v)}%)"
            hsv_var.set(hsv_value)
            
            # Update color display
            color_frame.configure(fg_color=hex_value)
        
        def pick_color():
            color = colorchooser.askcolor(title="Choose a color")
            if color[0]:  # color is ((r,g,b), hex)
                update_color_values(color[0])
        
        def copy_value(value):
            window.clipboard_clear()
            window.clipboard_append(value.get())
        
        # Color picker button
        ctk.CTkButton(window, text="Pick Color", 
                     command=pick_color).pack(pady=10)
        
        # Copy buttons
        copy_frame = ctk.CTkFrame(window)
        copy_frame.pack(pady=10)
        
        ctk.CTkButton(copy_frame, text="Copy Hex", 
                     command=lambda: copy_value(hex_var)).pack(side="left", padx=5)
        ctk.CTkButton(copy_frame, text="Copy RGB", 
                     command=lambda: copy_value(rgb_var)).pack(side="left", padx=5)
        ctk.CTkButton(copy_frame, text="Copy HSV", 
                     command=lambda: copy_value(hsv_var)).pack(side="left", padx=5)
    
    return open_picker

def timer():
    def open_timer():
        window = ctk.CTkToplevel()
        window.title("Timer")
        window.geometry("300x400")
        
        # Time input frame
        input_frame = ctk.CTkFrame(window)
        input_frame.pack(padx=10, pady=10, fill="x")
        
        # Time inputs
        hours_var = ctk.StringVar(value="0")
        minutes_var = ctk.StringVar(value="0")
        seconds_var = ctk.StringVar(value="0")
        
        def create_time_input(text, variable):
            frame = ctk.CTkFrame(input_frame)
            frame.pack(side="left", expand=True)
            ctk.CTkLabel(frame, text=text).pack()
            entry = ctk.CTkEntry(frame, textvariable=variable, width=50, justify="center")
            entry.pack(pady=5)
            return entry
        
        hours_entry = create_time_input("Hours", hours_var)
        minutes_entry = create_time_input("Minutes", minutes_var)
        seconds_entry = create_time_input("Seconds", seconds_var)
        
        # Display
        display_var = ctk.StringVar(value="00:00:00")
        ctk.CTkLabel(window, textvariable=display_var, 
                    font=("Helvetica", 36)).pack(pady=20)
        
        # Timer state
        timer_running = False
        end_time = None
        
        def update_display():
            if timer_running and end_time:
                remaining = end_time - datetime.now()
                if remaining.total_seconds() <= 0:
                    display_var.set("00:00:00")
                    window.bell()  # Make a sound
                    stop_timer()
                else:
                    hours = remaining.seconds // 3600
                    minutes = (remaining.seconds % 3600) // 60
                    seconds = remaining.seconds % 60
                    display_var.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
                    window.after(1000, update_display)
        
        def start_timer():
            nonlocal timer_running, end_time
            if not timer_running:
                try:
                    hours = int(hours_var.get())
                    minutes = int(minutes_var.get())
                    seconds = int(seconds_var.get())
                    
                    if hours == 0 and minutes == 0 and seconds == 0:
                        return
                    
                    duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                    end_time = datetime.now() + duration
                    timer_running = True
                    start_btn.configure(text="Pause")
                    update_display()
                except ValueError:
                    tk.messagebox.showerror("Error", "Please enter valid numbers")
            else:
                timer_running = False
                start_btn.configure(text="Start")
        
        def stop_timer():
            nonlocal timer_running, end_time
            timer_running = False
            end_time = None
            display_var.set("00:00:00")
            start_btn.configure(text="Start")
            hours_var.set("0")
            minutes_var.set("0")
            seconds_var.set("0")
        
        # Control buttons
        btn_frame = ctk.CTkFrame(window)
        btn_frame.pack(pady=20)
        
        start_btn = ctk.CTkButton(btn_frame, text="Start", command=start_timer)
        start_btn.pack(side="left", padx=5)
        
        stop_btn = ctk.CTkButton(btn_frame, text="Stop", command=stop_timer)
        stop_btn.pack(side="left", padx=5)
    
    return open_timer

def get_tools():
    return [
        {
            "name": "Calculator",
            "description": "Scientific calculator with basic and advanced functions",
            "callback": calculator()
        },
        {
            "name": "Unit Converter",
            "description": "Convert between different units of measurement",
            "callback": unit_converter()
        },
        {
            "name": "Color Picker",
            "description": "Pick colors and get their hex, RGB, and HSV values",
            "callback": color_picker()
        },
        {
            "name": "Timer",
            "description": "Countdown timer with hours, minutes, and seconds",
            "callback": timer()
        }
    ]
