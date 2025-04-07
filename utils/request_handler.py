import requests
import json
from urllib.parse import urlparse, parse_qs
from config.settings import REQUEST_TIMEOUT

class RequestHandler:
    def __init__(self, logger):
        self.logger = logger
    
    def parse_url(self, url):
        """Parse URL and return parameters"""
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        return params
    
    def parse_headers(self, headers_text):
        """Parse headers text into dictionary"""
        headers = {}
        for line in headers_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        return headers
    
    def convert_browse_url(self, url):
        """Convert browse URL to API URL"""
        if "/browse" in url:
            api_url = url.replace("/browse", "/secure/titles")
            self.logger.info(f"Converting browse URL to API URL: {api_url}")
            return api_url
        return url
    
    def make_request(self, url, method, headers):
        """Make HTTP request and return response"""
        try:
            api_url = self.convert_browse_url(url)
            self.logger.info(f"Making {method} request with headers: {headers}")
            
            response = requests.request(
                method,
                api_url,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            self.logger.info(f"Request successful with status code: {response.status_code}")
            
            return response
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            if hasattr(e.response, 'text'):
                error_msg += f"\nResponse: {e.response.text}"
            self.logger.error(error_msg)
            raise
    
    def validate_response(self, response):
        """Validate response and return JSON data"""
        try:
            response_data = response.json()
            if not response_data:
                raise ValueError("Empty response received")
            self.logger.info("Successfully parsed JSON response")
            return response_data
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON response: {str(e)}"
            self.logger.error(error_msg)
            raise 