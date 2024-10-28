import atexit
import logging
import urllib3
import time
from pathlib import Path
from typing import Any, List
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException
)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed
)
from urllib3.exceptions import MaxRetryError, NewConnectionError
from webdriver_manager.chrome import ChromeDriverManager

from selenium_base.core.logger import logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.ERROR)
logging.getLogger('urllib3.util.retry').setLevel(logging.ERROR)
logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)
http = urllib3.PoolManager(retries=False)


class DriverManager:
    def __init__(self, headless: bool = True, implicit_wait: int = 10, page_load_timeout: int = 30) -> None:
        self.headless = headless
        self.implicit_wait = implicit_wait
        self.page_load_timeout = page_load_timeout
        self.driver = self._initialize_driver()
        atexit.register(self.quit_driver)

    def _initialize_driver(self):
        """Initializes the ChromeDriver using webdriver_manager."""
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(self.implicit_wait)
        driver.set_page_load_timeout(self.page_load_timeout)
        return driver
    
    def quit_driver(self):
        """Closes the driver safely."""
        if self.driver:
            try:
                self.driver.quit()
            except (WebDriverException, MaxRetryError, NewConnectionError) as e:
                logger.error(f"Error while quitting WebDriver: {e}")
        else:
            logger.warning("No WebDriver instance to quit.")

    retry_decorator = retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(5),
        retry=retry_if_exception_type((NoSuchElementException, TimeoutException, WebDriverException)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True
    )

    @retry_decorator
    def get(self, url: str) -> None:
        """Navigates to a specified URL with retries."""
        logger.info(f"Navigating to {url}...")
        self.driver.get(url)
    
    def wait(self, seconds: float) -> None:
        """Pauses execution for a specified number of seconds."""
        logger.info(f"Waiting for {seconds} seconds...")
        time.sleep(seconds)

    @retry_decorator
    def refresh(self):
        """Refreshes the current page."""
        logger.info("Refreshing the page...")
        self.driver.refresh()

    @retry_decorator
    def back(self):
        """Navigates back in browser history."""
        logger.info("Navigating back in history...")
        self.driver.back()

    @retry_decorator
    def forward(self):
        """Navigates forward in browser history."""
        logger.info("Navigating forward in history...")
        self.driver.forward()

    @retry_decorator
    def find_element(self, by: By, value: str) -> WebElement:
        """Finds an element on the page with retries."""
        logger.info(f"Finding element by {by} with value '{value}'")
        return self.driver.find_element(by, value)

    @retry_decorator
    def find_elements(self, by: By, value: str) -> List[WebElement]:
        """Finds multiple elements on the page with retries."""
        logger.info(f"Finding elements by {by} with value '{value}'")
        return self.driver.find_elements(by, value)

    @retry_decorator
    def click_element(self, by: By, value: str) -> None:
        """Finds and clicks an element on the page with retries."""
        element = self.find_element(by, value)
        logger.info(f"Clicking element with {by}='{value}'")
        element.click()

    @retry_decorator
    def send_keys_to_element(self, by: By, value: str, keys: str) -> None:
        """Finds an element and sends keys to it with retries."""
        element = self.find_element(by, value)
        logger.info(f"Sending keys to element with {by}='{value}'")
        element.send_keys(keys)

    @retry_decorator
    def clear_element(self, by: By, value: str) -> None:
        """Clears text from an input field with retries."""
        element = self.find_element(by, value)
        logger.info(f"Clearing element with {by}='{value}'")
        element.clear()

    # JavaScript execution
    @retry_decorator
    def execute_script(self, script: str, *args) -> Any:
        """Executes JavaScript on the current page with retries."""
        logger.info(f"Executing script: {script}")
        return self.driver.execute_script(script, *args)

    def close_window(self) -> None:
        """Closes the current window."""
        logger.info("Closing the current window...")
        try:
            self.driver.close()
        except (WebDriverException, MaxRetryError, NewConnectionError) as e:
            logger.error(f"Error while closing window: {e}")

    # Scrolling
    @retry_decorator
    def scroll_to_bottom(self) -> None:
        """Scrolls to the bottom of the page."""
        logger.info("Scrolling to the bottom of the page...")
        last_height = self.execute_script("return document.body.scrollHeight")
        while True:
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for page to load
            new_height = self.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    @retry_decorator
    def accept_alert(self) -> None:
        """Accepts the alert box."""
        logger.info("Accepting alert...")
        alert = self.driver.switch_to.alert
        alert.accept()

    @retry_decorator
    def dismiss_alert(self) -> None:
        """Dismisses the alert box."""
        logger.info("Dismissing alert...")
        alert = self.driver.switch_to.alert
        alert.dismiss()

    # File upload
    @retry_decorator
    def upload_file(self, by: By, value: str, file_path: Path | str) -> None:
        """Uploads a file by sending the file path to the input element."""
        logger.info(f"Uploading file '{file_path}' to element with {by}='{value}'")
        element = self.find_element(by, value)
        element.send_keys(file_path)

