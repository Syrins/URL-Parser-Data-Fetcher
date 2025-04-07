import os
import json
from datetime import datetime
from urllib.parse import urlparse
from config.settings import DATA_DIR

class FileManager:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
    
    def create_directory_structure(self, url):
        """Create directory structure based on URL"""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        path_parts = parsed_url.path.strip('/').split('/')
        
        # Create domain directory
        domain_dir = os.path.join(DATA_DIR, domain)
        os.makedirs(domain_dir, exist_ok=True)
        
        # Create path directories
        current_dir = domain_dir
        for part in path_parts:
            if part:
                current_dir = os.path.join(current_dir, part)
                os.makedirs(current_dir, exist_ok=True)
        
        return current_dir
    
    def save_response(self, url, response_data):
        """Save response data to file"""
        save_dir = self.create_directory_structure(url)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"response_{timestamp}.json"
        filepath = os.path.join(save_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(response_data, f, indent=4, ensure_ascii=False)
        
        return filepath
    
    def load_response(self, filepath):
        """Load response data from file"""
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def get_all_responses(self):
        """Get all saved response files"""
        responses = []
        for root, _, files in os.walk(DATA_DIR):
            for file in files:
                if file.endswith('.json') and file.startswith('response_'):
                    filepath = os.path.join(root, file)
                    try:
                        data = self.load_response(filepath)
                        
                        # Extract timestamp correctly from filename
                        # Format should be: response_YYYYMMDD_HHMMSS.json
                        timestamp_part = file[9:-5]  # Remove 'response_' and '.json'
                        
                        responses.append({
                            'filepath': filepath,
                            'data': data,
                            'timestamp': timestamp_part
                        })
                    except Exception as e:
                        continue
        return sorted(responses, key=lambda x: x['timestamp'], reverse=True) 