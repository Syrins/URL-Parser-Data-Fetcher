import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
import tkinter as tk
from config.settings import LOGS_DIR, LOG_FORMAT, LOG_FILE_MAX_SIZE, LOG_FILE_BACKUP_COUNT

class GUILogHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        
    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.see(tk.END)
        self.text_widget.after(0, append)

def setup_logging(log_text_widget):
    """Set up logging configuration"""
    # Create logs directory if it doesn't exist
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    # Configure logging
    log_file = os.path.join(LOGS_DIR, f"url_parser_{datetime.now().strftime('%Y%m%d')}.log")
    
    # Create handlers
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=LOG_FILE_MAX_SIZE,
        backupCount=LOG_FILE_BACKUP_COUNT,
        encoding='utf-8'
    )
    
    # Create formatters and add it to handlers
    log_format = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(log_format)
    
    # Get the logger
    logger = logging.getLogger('URLParser')
    logger.setLevel(logging.DEBUG)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    
    # Add GUI handler
    gui_handler = GUILogHandler(log_text_widget)
    gui_handler.setFormatter(log_format)
    logger.addHandler(gui_handler)
    
    return logger 