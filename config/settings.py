import os

# Application settings
APP_NAME = "URL Parser & Data Fetcher"
APP_VERSION = "1.0.0"
WINDOW_SIZE = "1400x900"
WINDOW_MIN_SIZE = (1000, 700)

# Theme settings
THEME_MODE = "dark"
THEME_COLOR = "blue"

# UI settings
FONT_FAMILY = "Helvetica"
FONT_SIZES = {
    "small": 12,
    "medium": 14,
    "large": 16,
    "title": 20,
    "header": 18
}

# Color settings
COLORS = {
    "primary": "#3a7ebf",
    "secondary": "#2CC985",
    "error": "#E63946",
    "warning": "#F4A261",
    "info": "#61A4BC",
    "success": "#2CC985",
}

# Directory settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "veriler")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Logging settings
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_FILE_BACKUP_COUNT = 5

# Request settings
REQUEST_TIMEOUT = 30

# Default headers
DEFAULT_HEADERS = """
accept: application/json, text/plain, */*
accept-encoding: gzip, deflate, br, zstd
accept-language: tr;q=0.6
cache-control: no-cache
pragma: no-cache
priority: u=1, i
sec-ch-ua: "Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"
sec-ch-ua-arch: "x86"
sec-ch-ua-bitness: "64"
sec-ch-ua-full-version-list: "Chromium";v="134.0.0.0", "Not:A-Brand";v="24.0.0.0", "Brave";v="134.0.0.0"
sec-ch-ua-mobile: ?0
sec-ch-ua-model: ""
sec-ch-ua-platform: "Windows"
sec-ch-ua-platform-version: "10.0.0"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
sec-gpc: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36
x-e-h: Cbn+FK3kIIO1c8QZFeYpu0vo0UjG0YtgED8ukkHaqAzGMBivfuFqYv/KhrhzROFdQ6YQBaZ6Glqq8s5uLCV7/10NHc6N9eoZROJDYhYzUYqahZ4o/U8=.nfyT610BqhHmTI8m
""" 