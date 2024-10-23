
# Selenium Example Project

This project demonstrates a Selenium WebDriver implementation with structured logging, retry mechanisms, and Pydantic models.

## Project Structure

```
selenium_example/
├── selenium_base/
│   └── core/
│       ├── base.py         # DriverManager implementation
│       ├── logger.py       # Logging configuration
│       └── schema.py       # Pydantic BaseModel
└── main.py                 # Example usage
```

## Features

- Chrome WebDriver with session management
- Automatic driver installation and cleanup
- Structured logging with rotation
- Pydantic models for data validation
- Retry mechanisms for web interactions
- Comprehensive error handling and logging
- Headless mode support

## Usage

```python
from selenium_base.core.base import DriverManager
from selenium_base.core.logger import logger

def main():
    driver = DriverManager(headless=False)
    
    try:
        driver.get("https://www.google.com")
        search_bar = driver.find_element("name", "q")
        search_bar.send_keys("Aimleap")
        search_bar.submit()
        driver.scroll_to_bottom()
        logger.info("Successfully performed Google search")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        
    finally:
        driver.quit_driver()

if __name__ == "__main__":
    main()
```

## Components

### DriverManager (base.py)
- Manages Chrome WebDriver sessions
- Handles automatic driver installation
- Implements retry mechanisms
- Provides comprehensive web interaction methods
- Supports JavaScript execution
- Includes error handling and logging

### Logger (logger.py)
- Configurable logging levels
- File rotation support
- Formatted log output
- Daily log files with retention

### Schema Models (schema.py)
- Pydantic BaseModel implementation
- Type hints and field validation
- Custom field aliases
- JSON encoding support
- Attribute-based model creation

## Key Features

- Automatic WebDriver management
- Retry mechanism for failed operations
- Headless browser support
- Page navigation controls
- Element interaction methods
- File upload handling
- Alert management
- Scrolling functionality
- Custom JavaScript execution
- Comprehensive error handling

## Requirements

- Python 3.7+
- selenium
- webdriver-manager
- pydantic
- tenacity
- logging

## Requirements Installation
```bash
pip install -r requirements.txt
```
