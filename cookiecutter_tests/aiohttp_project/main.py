"""AIOHTTP Project

This module serves as the main entry point for:

A AIOHTTP web scraper
"""

__author__ = "Your Name"
__email__ = "your.email@example.com"
__version__ = "0.0.1"


import asyncio
import json
from typing import NoReturn

from aio_http.core.base import AioHttpClientManager
from aio_http.core.logger import logger

from config import Config


async def main() -> NoReturn:
    """A AIOHTTP web scraper"""
    url = "https://v2.jokeapi.dev/joke/Any"
    outputfile = Config.OUTPUT_FILE
    try:
        # Your main application logic here
        client = AioHttpClientManager()
        client.set_headers(Config.HEADERS)
        client.set_proxies(Config.PROXIES)
        
        response = await client.send_request(url)
        print(json.loads(response))
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


def run() -> None:
    """Execute the main application."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
    