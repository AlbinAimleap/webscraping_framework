import tls_client
import json
import logging
import asyncio
from typing import Dict, Any, Optional, List, Tuple, Literal

from tlsclient.core.logger import logger

class TLSClientManager:
    def __init__(self, client_identifier: str, async_mode: bool = False):
        """
        Initializes the TLSClientManager with optional client identifier and async mode.
        """
        self.session = tls_client.Session(client_identifier=client_identifier)
        self.async_mode = async_mode
        logger.info("TLSClientManager initialized. Async mode: %s", self.async_mode)

    def set_headers(self, headers: Dict[str, str]) -> None:
        """
        Sets headers for the TLS session.
        """
        self.session.headers.update(headers)
        logger.info("Headers set: %s", headers)

    def set_proxies(self, proxies: Dict[str, str]) -> None:
        """
        Sets proxies for the TLS session.
        """
        self.session.proxies = proxies
        logger.info("Proxies set: %s", proxies)

    async def async_request(self, method: str, url: str, **kwargs: Any) -> tls_client.response.Response:
        """
        Asynchronously sends an HTTP request to the specified URL using the given method.
        """
        logger.info("Sending async %s request to %s", method.upper(), url)

        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: getattr(self.session, method.lower())(url, **kwargs))
            logger.info("Async request to %s returned status code: %d", url, response.status_code)
            return response
        except Exception as e:
            logger.error("Error sending async request: %s", e)
            raise

    def sync_request(self, method: str, url: str, **kwargs: Any) -> tls_client.response.Response:
        """
        Sends a synchronous HTTP request to the specified URL using the given method.
        """
        logger.info("Sending %s request to %s", method.upper(), url)

        try:
            response = getattr(self.session, method.lower())(url, **kwargs)
            logger.info("Request to %s returned status code: %d", url, response.status_code)
            return response
        except Exception as e:
            logger.error("Error sending request: %s", e)
            raise


    def close(self) -> None:
        """
        Closes the TLS session.
        """
        self.session.close()
        logger.info("TLS session closed.")

class HTTPClient:
    def __init__(self, client_identifier: str = "chrome_108", async_mode: bool = False):
        self.client_manager = TLSClientManager(client_identifier, async_mode)

    def set_headers(self, headers: Dict[str, str]) -> None:
        self.client_manager.set_headers(headers)

    def set_proxies(self, proxies: Dict[str, str]) -> None:
        self.client_manager.set_proxies(proxies)

    async def send_async_request(self, url: str, method: str = "GET", **kwargs: Any) -> Dict[str, Any]:
        response = await self.client_manager.async_request(method, url, **kwargs)
        return response

    def send_request(self, url: str, method: str = "GET", **kwargs: Any) -> Dict[str, Any]:
        response = self.client_manager.sync_request(method, url, **kwargs)
        return response

    async def send_multi_request(self, urls: List[str], method: Literal["GET", "POST"] = "GET") -> List[Dict[str, Any]]:
        tasks = [self.async_request(method, url) for url in urls]
        return await asyncio.gather(*tasks)
    
    def close(self) -> None:
        self.client_manager.close()

