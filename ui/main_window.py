import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from config.settings import APP_NAME, WINDOW_SIZE, THEME_MODE, THEME_COLOR
from ui.tabs.request_tab import RequestTab
from ui.tabs.data_viewer_tab import DataViewerTab

class MainWindow(ctk.CTk):
    def __init__(self, logger, request_handler, file_manager):
        super().__init__()
        
        self.logger = logger
        self.request_handler = request_handler
        self.file_manager = file_manager
        
        self.current_view = None
        self.setup_window()
        self.setup_ui()
    
    def setup_window(self):
        """Set up window properties"""
        self.title(APP_NAME)
        self.geometry(WINDOW_SIZE)
        
        # Set theme
        ctk.set_appearance_mode(THEME_MODE)
        ctk.set_default_color_theme(THEME_COLOR)
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
    
    def setup_ui(self):
        """Set up UI components with a modern sidebar design"""
        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # Add logo/title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text=APP_NAME, 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Add navigation buttons
        self.request_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="API Request",
            font=ctk.CTkFont(size=14),
            fg_color="transparent", 
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.show_request_view
        )
        self.request_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.data_viewer_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="Data Viewer",
            font=ctk.CTkFont(size=14),
            fg_color="transparent", 
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.show_data_viewer
        )
        self.data_viewer_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Add theme switcher
        self.appearance_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Appearance Mode:", 
            anchor="w"
        )
        self.appearance_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.appearance_option = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode
        )
        self.appearance_option.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="w")
        self.appearance_option.set(THEME_MODE.capitalize())
        
        # Create main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Create frame for tab content
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Create log frame at bottom
        self.log_frame = ctk.CTkFrame(self.main_frame)
        self.log_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.log_label = ctk.CTkLabel(
            self.log_frame,
            text="Log Messages",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.log_label.pack(pady=5, padx=10, anchor="w")
        
        self.log_text = ctk.CTkTextbox(
            self.log_frame,
            height=100,
            font=("Consolas", 12)
        )
        self.log_text.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Initialize the tabs (but don't display them yet)
        self.request_tab = RequestTab(
            self.content_frame,
            self.logger,
            self.request_handler,
            self.file_manager,
            self.on_response_saved
        )
        
        self.data_viewer_tab = DataViewerTab(
            self.content_frame,
            self.file_manager
        )
        
        # Show the request view by default
        self.show_request_view()
    
    def show_request_view(self):
        """Show the request view and hide other views"""
        if self.current_view:
            self.current_view.pack_forget()
        
        self.content_title = ctk.CTkLabel(
            self.main_frame,
            text="API Request",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.content_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        self.request_tab.pack(fill="both", expand=True)
        self.current_view = self.request_tab
        
        # Highlight active button
        self.request_button.configure(fg_color=("gray75", "gray25"))
        self.data_viewer_button.configure(fg_color="transparent")
    
    def show_data_viewer(self):
        """Show the data viewer and hide other views"""
        if self.current_view:
            self.current_view.pack_forget()
        
        self.content_title = ctk.CTkLabel(
            self.main_frame,
            text="Data Viewer",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.content_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Refresh data viewer before showing
        self.data_viewer_tab.refresh()
        self.data_viewer_tab.pack(fill="both", expand=True)
        self.current_view = self.data_viewer_tab
        
        # Highlight active button
        self.data_viewer_button.configure(fg_color=("gray75", "gray25"))
        self.request_button.configure(fg_color="transparent")
    
    def change_appearance_mode(self, new_appearance_mode):
        """Change the appearance mode"""
        ctk.set_appearance_mode(new_appearance_mode)
    
    def on_response_saved(self):
        """Handle new response saved event"""
        # If data viewer is visible, refresh it
        if self.current_view == self.data_viewer_tab:
            self.data_viewer_tab.refresh() 