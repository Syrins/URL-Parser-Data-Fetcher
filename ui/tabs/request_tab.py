import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
from config.settings import DEFAULT_HEADERS

class RequestTab(ctk.CTkFrame):
    def __init__(self, parent, logger, request_handler, file_manager, on_response_saved):
        super().__init__(parent)
        self.logger = logger
        self.request_handler = request_handler
        self.file_manager = file_manager
        self.on_response_saved = on_response_saved
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create scrollable frame for all content
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Method & URL section
        self.url_section = ctk.CTkFrame(self.scrollable_frame)
        self.url_section.pack(fill="x", padx=10, pady=10)
        
        self.url_section_label = ctk.CTkLabel(
            self.url_section, 
            text="API Request URL", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.url_section_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Method and URL in one row
        self.request_row = ctk.CTkFrame(self.url_section)
        self.request_row.pack(fill="x", padx=10, pady=5)
        
        self.method_var = tk.StringVar(value="GET")
        self.method_menu = ctk.CTkOptionMenu(
            self.request_row,
            values=["GET", "POST", "PUT", "DELETE", "PATCH"],
            variable=self.method_var,
            width=100,
            dropdown_font=ctk.CTkFont(size=13)
        )
        self.method_menu.pack(side="left", padx=(0, 10))
        
        self.url_entry = ctk.CTkEntry(
            self.request_row,
            placeholder_text="https://example.com/path?param1=value1&param2=value2",
            height=32,
            font=ctk.CTkFont(size=13)
        )
        self.url_entry.pack(side="left", fill="x", expand=True)
        
        # Parse Button
        self.parse_button = ctk.CTkButton(
            self.url_section,
            text="Send Request",
            command=self.parse_and_fetch,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8
        )
        self.parse_button.pack(pady=15, padx=10)
        
        # Headers Section
        self.headers_section = ctk.CTkFrame(self.scrollable_frame)
        self.headers_section.pack(fill="x", padx=10, pady=10)
        
        self.headers_label = ctk.CTkLabel(
            self.headers_section,
            text="Request Headers",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.headers_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.headers_text = ctk.CTkTextbox(
            self.headers_section,
            height=150,
            font=("Consolas", 12),
            corner_radius=8
        )
        self.headers_text.pack(fill="x", padx=10, pady=10)
        self.headers_text.insert("1.0", DEFAULT_HEADERS)
        
        # Parameters Display
        self.params_section = ctk.CTkFrame(self.scrollable_frame)
        self.params_section.pack(fill="x", padx=10, pady=10)
        
        self.params_label = ctk.CTkLabel(
            self.params_section,
            text="URL Parameters",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.params_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.params_text = ctk.CTkTextbox(
            self.params_section,
            height=150,
            font=("Consolas", 12),
            corner_radius=8
        )
        self.params_text.pack(fill="x", padx=10, pady=10)
        
        # Response Preview
        self.response_section = ctk.CTkFrame(self.scrollable_frame)
        self.response_section.pack(fill="x", padx=10, pady=10)
        
        self.response_label = ctk.CTkLabel(
            self.response_section,
            text="Response Preview",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.response_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.response_preview = ctk.CTkTextbox(
            self.response_section,
            height=150,
            font=("Consolas", 12),
            corner_radius=8,
            state="disabled"
        )
        self.response_preview.pack(fill="x", padx=10, pady=10)
        
        # Status Section
        self.status_section = ctk.CTkFrame(self.scrollable_frame)
        self.status_section.pack(fill="x", padx=10, pady=10)
        
        self.status_label = ctk.CTkLabel(
            self.status_section,
            text="Ready to send request",
            font=ctk.CTkFont(size=14),
            text_color=("gray40", "gray60")
        )
        self.status_label.pack(padx=10, pady=10)
    
    def parse_and_fetch(self):
        url = self.url_entry.get()
        if not url:
            self.logger.error("No URL provided")
            messagebox.showerror("Error", "Please enter a URL")
            return
            
        try:
            self.logger.info(f"Processing URL: {url}")
            self.status_label.configure(text="Processing request...", text_color=("blue", "#3a7ebf"))
            
            # Parse URL and parameters
            params = self.request_handler.parse_url(url)
            
            # Display parameters
            params_text = "URL Parameters:\n\n"
            for key, value in params.items():
                params_text += f"{key}: {value[0]}\n"
            
            self.params_text.delete("1.0", "end")
            self.params_text.insert("1.0", params_text)
            
            # Parse headers
            headers = self.request_handler.parse_headers(self.headers_text.get("1.0", "end-1c"))
            
            # Make request
            method = self.method_var.get().lower()
            response = self.request_handler.make_request(url, method, headers)
            
            # Validate and get response data
            response_data = self.request_handler.validate_response(response)
            
            # Update response preview
            self.response_preview.configure(state="normal")
            self.response_preview.delete("1.0", "end")
            self.response_preview.insert("1.0", json.dumps(response_data, indent=2, ensure_ascii=False))
            self.response_preview.configure(state="disabled")
            
            # Save response
            filepath = self.file_manager.save_response(url, response_data)
            
            # Update status
            success_msg = f"Request successful. Data saved to {filepath}"
            self.logger.info(success_msg)
            self.status_label.configure(text=success_msg, text_color=("green", "#2CC985"))
            
            # Notify parent about new response
            self.on_response_saved()
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            self.status_label.configure(text=error_msg, text_color=("red", "#E63946"))
            messagebox.showerror("Error", error_msg) 