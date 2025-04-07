import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import syntax_highlighting as sh
import os

class DataViewerTab(ctk.CTkFrame):
    def __init__(self, parent, file_manager):
        super().__init__(parent)
        self.file_manager = file_manager
        
        # Set styles for treeview
        self.set_treeview_style()
        
        self.setup_ui()
        self.load_responses()
    
    def set_treeview_style(self):
        """Configure styles for the treeview widget"""
        style = ttk.Style()
        style.theme_use("default")
        
        # Configure the Treeview widget
        style.configure(
            "Custom.Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            borderwidth=0,
            rowheight=30
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", "#1f538d")]
        )
        
        # Configure the Treeview heading
        style.configure(
            "Custom.Treeview.Heading",
            background="#1a1a1a",
            foreground="white",
            relief="flat",
            borderwidth=0
        )
        style.map(
            "Custom.Treeview.Heading",
            background=[("active", "#2a2a2a")]
        )
    
    def setup_ui(self):
        # Create main container with left and right frames
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create grid-based layout
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.columnconfigure(1, weight=2)
        self.main_container.rowconfigure(0, weight=1)
        
        # Left frame for file browser
        self.left_frame = ctk.CTkFrame(self.main_container)
        self.left_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        # Search and refresh section
        self.search_frame = ctk.CTkFrame(self.left_frame)
        self.search_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        self.file_label = ctk.CTkLabel(
            self.search_frame,
            text="Saved Responses",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.file_label.pack(side="left", padx=10, pady=10)
        
        self.refresh_button = ctk.CTkButton(
            self.search_frame,
            text="↻",
            width=30,
            height=30,
            corner_radius=8,
            command=self.refresh
        )
        self.refresh_button.pack(side="right", padx=10, pady=10)
        
        # Treeview Frame
        self.tree_frame = ctk.CTkFrame(self.left_frame)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create custom treeview
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("Datetime", "Path"),
            show="headings",
            selectmode="browse",
            style="Custom.Treeview"
        )
        
        # Configure columns
        self.tree.heading("Datetime", text="Datetime")
        self.tree.heading("Path", text="Location")
        self.tree.column("Datetime", width=140)
        self.tree.column("Path", width=160)
        
        # Add scrollbars
        self.tree_y_scroll = ctk.CTkScrollbar(
            self.tree_frame,
            command=self.tree.yview
        )
        self.tree_y_scroll.pack(side="right", fill="y")
        
        self.tree_x_scroll = ctk.CTkScrollbar(
            self.tree_frame,
            orientation="horizontal",
            command=self.tree.xview
        )
        self.tree_x_scroll.pack(side="bottom", fill="x")
        
        # Configure tree with scrollbars
        self.tree.configure(
            yscrollcommand=self.tree_y_scroll.set,
            xscrollcommand=self.tree_x_scroll.set
        )
        self.tree.pack(fill="both", expand=True)
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Right frame for JSON viewer
        self.right_frame = ctk.CTkFrame(self.main_container)
        self.right_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        # File info section
        self.file_info_frame = ctk.CTkFrame(self.right_frame)
        self.file_info_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        self.file_path_label = ctk.CTkLabel(
            self.file_info_frame,
            text="No file selected",
            font=ctk.CTkFont(size=14)
        )
        self.file_path_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Create JSON Editor
        self.editor_frame = ctk.CTkFrame(self.right_frame)
        self.editor_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.json_editor = scrolledtext.ScrolledText(
            self.editor_frame,
            wrap=tk.WORD,
            font=("Consolas", 12),
            bg="#2b2b2b",
            fg="white",
            insertbackground="white",
            selectbackground="#4a4a4a",
            selectforeground="white"
        )
        self.json_editor.pack(fill="both", expand=True, padx=5, pady=5)
    
    def format_timestamp(self, timestamp):
        """Format timestamp for display"""
        # Input might be like: 20250327_210714
        try:
            if "_" in timestamp:
                date_part, time_part = timestamp.split("_")
                
                # Format date part: YYYYMMDD -> YYYY-MM-DD
                year = date_part[0:4]
                month = date_part[4:6]
                day = date_part[6:8]
                
                # Format time part: HHMMSS -> HH:MM:SS
                hour = time_part[0:2]
                minute = time_part[2:4]
                second = time_part[4:6] if len(time_part) >= 6 else "00"
                
                return f"{year}-{month}-{day} {hour}:{minute}:{second}"
            else:
                # Handle case where timestamp doesn't contain underscore
                if len(timestamp) >= 8:
                    year = timestamp[0:4]
                    month = timestamp[4:6]
                    day = timestamp[6:8]
                    return f"{year}-{month}-{day}"
                
        except Exception:
            pass
        
        # Return original if formatting fails
        return timestamp
    
    def format_filepath(self, filepath):
        """Format filepath for display"""
        # Get just the domain and filename
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rel_path = os.path.relpath(filepath, basedir)
        
        # Return just the parent directory and filename
        parent_dir = os.path.basename(os.path.dirname(filepath))
        filename = os.path.basename(filepath)
        return f"{parent_dir}/{filename}"
    
    def load_responses(self):
        """Load all saved responses into the tree"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all responses
        responses = self.file_manager.get_all_responses()
        
        # Add to tree
        for response in responses:
            formatted_time = self.format_timestamp(response['timestamp'])
            formatted_path = self.format_filepath(response['filepath'])
            
            self.tree.insert(
                "",
                "end",
                values=(
                    formatted_time,
                    formatted_path
                ),
                tags=(response['filepath'],)
            )
    
    def on_select(self, event):
        """Handle file selection"""
        selection = self.tree.selection()
        if not selection:
            return
            
        item = self.tree.item(selection[0])
        filepath = self.tree.item(selection[0], "tags")[0]
        
        try:
            # Load and display data
            data = self.file_manager.load_response(filepath)
            
            # Update file path label
            self.file_path_label.configure(text=f"File: {filepath}")
            
            # Update editor
            self.update_preview(data)
        except Exception as e:
            self.json_editor.delete("1.0", tk.END)
            self.json_editor.insert("1.0", f"Error loading file: {str(e)}")
    
    def update_preview(self, data):
        """Update JSON preview with syntax highlighting"""
        # Format JSON
        formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
        
        # Clear existing content
        self.json_editor.delete("1.0", tk.END)
        
        # Insert formatted JSON
        self.json_editor.insert("1.0", formatted_json)
        
        # Apply syntax highlighting
        self.highlight_json()
    
    def highlight_json(self):
        """Apply syntax highlighting to JSON content"""
        # Configure tags
        self.json_editor.tag_configure("string", foreground="#ce9178")
        self.json_editor.tag_configure("number", foreground="#b5cea8")
        self.json_editor.tag_configure("boolean", foreground="#569cd6")
        self.json_editor.tag_configure("null", foreground="#569cd6")
        self.json_editor.tag_configure("key", foreground="#9cdcfe")
        
        # Apply highlighting
        content = self.json_editor.get("1.0", tk.END)
        self.json_editor.tag_remove("string", "1.0", tk.END)
        self.json_editor.tag_remove("number", "1.0", tk.END)
        self.json_editor.tag_remove("boolean", "1.0", tk.END)
        self.json_editor.tag_remove("null", "1.0", tk.END)
        self.json_editor.tag_remove("key", "1.0", tk.END)
        
        # Highlight strings
        for match in sh.find_strings(content):
            self.json_editor.tag_add("string", match[0], match[1])
            
        # Highlight numbers
        for match in sh.find_numbers(content):
            self.json_editor.tag_add("number", match[0], match[1])
            
        # Highlight booleans and null
        for match in sh.find_booleans(content):
            self.json_editor.tag_add("boolean", match[0], match[1])
            
        for match in sh.find_nulls(content):
            self.json_editor.tag_add("null", match[0], match[1])
            
        # Highlight keys
        for match in sh.find_keys(content):
            self.json_editor.tag_add("key", match[0], match[1])
    
    def refresh(self):
        """Refresh the file list"""
        self.load_responses() 