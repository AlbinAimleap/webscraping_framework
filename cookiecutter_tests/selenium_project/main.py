"""Selenium Project

This module serves as the main entry point for:

A Selenium web scraper
"""

__author__ = "Your Name"
__email__ = "your.email@example.com"
__version__ = "0.0.1"


import selenium
from selenium_base.core.base import DriverManager, logger
from selenium_base.core.logger import logger

from config import Config


def search_and_scroll(driver, url, search_query):
    """Searches for a query and scrolls to the bottom of the page."""
    driver.get(url)
    search_bar = driver.find_element("name", "q")
    search_bar.send_keys(search_query)
    search_bar.submit()
    driver.scroll_to_bottom()
    driver.wait(10)
        

def main():
    """A Selenium web scraper"""
    url = "https://google.com"
    outputfile = Config.OUTPUT_FILE
        
    try:
        driver = DriverManager(headless=False)
        search_and_scroll(driver, url, "Aimleap")
        logger.info("Successfully interacted with Google Search.")

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt detected. Exiting...")
        driver.quit_driver()
        
    except (selenium.common.exceptions.WebDriverException,
        selenium.common.exceptions.TimeoutException,
        selenium.common.exceptions.NoSuchElementException,
        selenium.common.exceptions.ElementNotInteractableException) as e:        logger.error(f"An error occurred during interaction: {e}")
        
    finally:
        logger.info("Quitting the WebDriver...")
        driver.quit_driver()
        logger.info("WebDriver quit successfully.")


if __name__ == "__main__":
    main()