import customtkinter as ctk

class ThemeManager:
    def __init__(self):
        self.current_theme = "dark"
        self.set_theme(self.current_theme)
        
    def set_theme(self, theme):
        if theme == "dark":
            ctk.set_appearance_mode("dark")
            self.colors = {
                "bg": "#1a1a1a",
                "fg": "#ffffff",
                "accent": "#00b4d8"
            }
        else:
            ctk.set_appearance_mode("light")
            self.colors = {
                "bg": "#ffffff",
                "fg": "#1a1a1a",
                "accent": "#0077b6"
            }
            
    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.set_theme(self.current_theme)
