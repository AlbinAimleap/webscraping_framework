import aiohttp
import asyncio
import json
from typing import Any, Dict, List, Optional

from aio_http.core.logger import logger

class AioHttpClientManager:
    def __init__(self) -> None:
        """
        Initializes the AioHttpClientManager with async mode.
        """
        self.session = None
        logger.info("AioHttpClientManager initialized")

    async def _init_session(self) -> None:
        """Initializes the aiohttp session."""
        if self.session is None:
            connector = aiohttp.TCPConnector(force_close=True)
            self.session = aiohttp.ClientSession(connector=connector)
            logger.info("AioHttp session created.")

    async def close(self) -> None:
        """Closes the aiohttp session."""
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

    async def send_request(self, url: str, method: str = "GET", **kwargs) -> str | None:
        """
        Asynchronously sends an HTTP request to the specified URL using the given method.
        """
        await self._init_session()
        logger.info("Sending async %s request to %s", method.upper(), url)

        try:
            async with self.session.request(method, url, **kwargs) as response:
                logger.info("Async request to %s returned status code: %d", url, response.status)
                return await response.text()
        except Exception as e:
            logger.error("Error sending async request: %s", e)
            return None

    async def send_multi_request(self, urls: List[str], method: str = "GET", **kwargs) -> List[str] | None:
        """
        Asynchronously loads a list of URLs and sends requests for each.
        """
        logger.info("Loading URLs for async requests: %s", urls)
        tasks = []
        for url in urls:
            tasks.append(self.send_request(url, method, **kwargs))

        # Await all tasks and gather responses
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("Loaded responses for %d URLs", len(urls))
        return responses if responses else None

    async def set_headers(self, headers) -> None:
        """
        Sets headers for the aiohttp session.
        """
        await self._init_session()
        self.session.headers.update(headers)
        logger.info("Headers set: %s", headers)
        
    async def set_proxies(self, proxies: Dict[str, str]) -> None:
        """
        Sets proxies for the aiohttp session.
        """
        # Proxy format: {"http": "http://proxy.com", "https": "https://proxy.com"}
        await self._init_session()
        self.session.proxies = proxies
        logger.info("Proxies set: %s", proxies)