import customtkinter as ctk
from tools import utility_tools, text_tools, image_tools, programming_tools, security_tools
from theme_manager import ThemeManager
import json
from pathlib import Path

class ToolboxApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Modern Toolbox")
        self.root.geometry("1000x600")
        
        # Theme manager
        self.theme_manager = ThemeManager()
        
        # Initialize UI components
        self.setup_ui()
        
        # Load bookmarks
        self.bookmarks = self.load_bookmarks()
        
    def setup_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self.root, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        # Search bar
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self.sidebar, 
            placeholder_text="Search tools...",
            textvariable=self.search_var
        )
        self.search_entry.pack(padx=10, pady=10, fill="x")
        
        # Category buttons
        categories = ["Utilities", "Text Tools", "Image Tools", 
                     "Programming Tools", "Security Tools"]
        
        for category in categories:
            btn = ctk.CTkButton(
                self.sidebar,
                text=category,
                command=lambda c=category: self.show_category(c)
            )
            btn.pack(padx=10, pady=5, fill="x")
        
        # Theme toggle
        self.theme_switch = ctk.CTkSwitch(
            self.sidebar,
            text="Dark Mode",
            command=self.toggle_theme
        )
        self.theme_switch.pack(padx=10, pady=10)
        
        # Main content area
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
    def show_category(self, category):
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Get tools for category
        tools = self.get_tools_for_category(category)
        
        # Display tools in grid
        for i, tool in enumerate(tools):
            tool_frame = self.create_tool_card(tool)
            tool_frame.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
    def create_tool_card(self, tool):
        card = ctk.CTkFrame(self.content_frame)
        
        # Tool name
        name_label = ctk.CTkLabel(card, text=tool["name"])
        name_label.pack(padx=10, pady=5)
        
        # Tool description
        desc_label = ctk.CTkLabel(card, text=tool["description"], wraplength=200)
        desc_label.pack(padx=10, pady=5)
        
        # Launch button
        launch_btn = ctk.CTkButton(
            card,
            text="Launch",
            command=lambda: self.launch_tool(tool)
        )
        launch_btn.pack(padx=10, pady=5)
        
        return card
        
    def toggle_theme(self):
        self.theme_manager.toggle_theme()
        
    def load_bookmarks(self):
        try:
            with open("bookmarks.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
            
    def save_bookmarks(self):
        try:
            with open("bookmarks.json", "w") as f:
                json.dump(self.bookmarks, f)
            print("Bookmarks saved successfully")
        except Exception as e:
            print(f"Error saving bookmarks: {str(e)}")
            
    def get_tools_for_category(self, category):
        try:
            category_map = {
                "Utilities": utility_tools.get_tools(),
                "Text Tools": text_tools.get_tools(),
                "Image Tools": image_tools.get_tools(),
                "Programming Tools": programming_tools.get_tools(),
                "Security Tools": security_tools.get_tools()
            }
            tools = category_map.get(category, [])
            if not tools:
                print(f"No tools found for category: {category}")
            return tools
        except Exception as e:
            print(f"Error getting tools for {category}: {str(e)}")
            return []

    def launch_tool(self, tool):
        try:
            if not tool:
                print("Error: Tool object is None")
                return
                
            if "callback" in tool:
                print(f"Launching tool: {tool.get('name', 'Unknown')}")
                tool["callback"]()
            else:
                print(f"No callback defined for tool: {tool.get('name', 'Unknown')}")
        except Exception as e:
            print(f"Error launching tool: {str(e)}")

    def run(self):
        # Show initial category
        self.show_category("Utilities")
        self.root.mainloop()

if __name__ == "__main__":
    app = ToolboxApp()
    app.run()
