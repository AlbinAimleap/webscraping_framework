import aiohttp
import asyncio
from typing import Any, Dict, List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from aio_http.core.logger import logger

class AioHttpClientManager:
    def __init__(self, max_concurrent_requests: int = 5, retries: int = 3) -> None:
        """
        Initializes the AioHttpClientManager with async mode and a semaphore
        to limit the number of concurrent requests.
        
        Args:
            max_concurrent_requests (int): Maximum number of concurrent requests allowed.
            retries (int): Number of retry attempts for failed requests.
        """
        self.session = None
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self.retries = retries
        logger.info("AioHttpClientManager initialized with max_concurrent_requests=%d, retries=%d", max_concurrent_requests, retries)

    async def _init_session(self) -> None:
        """Initializes the aiohttp session if it doesn't exist."""
        if self.session is None:
            connector = aiohttp.TCPConnector(force_close=True)
            self.session = aiohttp.ClientSession(connector=connector)
            logger.info("AioHttp session created.")

    async def close(self) -> None:
        """Closes the aiohttp session if it exists."""
        if self.session:
            await self.session.close()
            await asyncio.sleep(0.250)
            logger.info("AioHttp session closed.")

    async def __aenter__(self):
        """Async context manager enter."""
        await self._init_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    def _get_retry_decorator(self):
        """Returns a retry decorator based on the configured retry settings."""
        return retry(stop=stop_after_attempt(self.retries), wait=wait_exponential(multiplier=1, min=2, max=10))

    async def _send_request(self, url: str, method: str = "GET", **kwargs) -> Optional[str]:
        """Helper method to send an HTTP request, includes semaphore management."""
        async with self.semaphore:
            logger.info("Sending async %s request to %s", method.upper(), url)
            try:
                async with self.session.request(method, url, **kwargs) as response:
                    logger.info("Request to %s returned status code: %d", url, response.status)
                    return await response.text()
            except Exception as e:
                logger.error("Error sending async request: %s", e)
                return None

    @property
    def request(self):
        """A property to use the retry decorator for single requests."""
        @self._get_retry_decorator()
        async def inner(url: str, method: str = "GET", **kwargs) -> Optional[str]:
            await self._init_session()
            return await self._send_request(url, method, **kwargs)
        return inner

    async def multi_request(self, urls: List[str], method: str = "GET", **kwargs) -> Optional[List[str]]:
        """
        Asynchronously sends requests for a list of URLs.
        
        Args:
            urls (List[str]): The list of URLs to request.
            method (str): The HTTP method to use (default: "GET").
            **kwargs: Additional arguments to pass to the request.

        Returns:
            Optional[List[str]]: A list of response texts if successful, None otherwise.
        """
        logger.info("Loading URLs for async requests: %s", urls)
        tasks = [self.request(url, method, **kwargs) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("Loaded responses for %d URLs", len(urls))
        return responses if responses else None

    async def set_headers(self, headers: Dict[str, str]) -> None:
        """Sets headers for the aiohttp session."""
        await self._init_session()
        self.session.headers.update(headers)
        logger.info("Headers set: %s", headers)

    async def set_proxies(self, proxies: Dict[str, str]) -> None:
        """Sets proxies for the aiohttp session."""
        await self._init_session()
        self.session.proxies = proxies
        logger.info("Proxies set: %s", proxies)
