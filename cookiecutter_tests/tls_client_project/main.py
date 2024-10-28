"""TLS Client Project

This module serves as the main entry point for:

A TLS Client web scraper
"""

__author__ = "Your Name"
__email__ = "your.email@example.com"
__version__ = "0.0.1"


import json
import asyncio
from tlsclient.core.base import HTTPClient
from tlsclient.core.logger import logger

from config import Config


async def main() -> None:
    """A TLS Client web scraper"""
    url = "https://v2.jokeapi.dev/joke/Any"

    try:
        client = HTTPClient(async_mode=True)
        client.set_headers(Config.HEADERS)
        client.set_proxies(Config.PROXIES)
        
        response = await client.send_async_request(url)
        
        print(response.json())

    except (json.JSONDecodeError, Exception) as e:
        logger.error("An error occurred: %s", e)
        
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
