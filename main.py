from ui.main_window import MainWindow
from utils.logger import setup_logging
from utils.request_handler import RequestHandler
from utils.file_manager import FileManager
from config.settings import WINDOW_MIN_SIZE
import os
import customtkinter as ctk

def main():
    # Create necessary directories
    from config.settings import DATA_DIR, LOGS_DIR
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    # Create file manager
    file_manager = FileManager()
    
    # Create main window
    window = MainWindow(None, None, file_manager)
    window.minsize(WINDOW_MIN_SIZE[0], WINDOW_MIN_SIZE[1])
    
    # Set up logging after log text widget is created
    logger = setup_logging(window.log_text)
    
    # Create request handler
    request_handler = RequestHandler(logger)
    
    # Update window with logger and request handler
    window.logger = logger
    window.request_handler = request_handler
    
    # Update request tab
    window.request_tab.logger = logger
    window.request_tab.request_handler = request_handler
    
    # Start application
    logger.info("Application started")
    window.mainloop()
    logger.info("Application closed")

if __name__ == "__main__":
    main() 