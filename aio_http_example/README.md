# AioHttp Example Project

This project demonstrates an asynchronous HTTP client implementation using `aiohttp` with structured logging and Pydantic models.

## Project Structure

```
aio_http_example/
├── aio_http/
│   └── core/
│       ├── base.py         # AioHttpClientManager implementation
│       ├──logger.py        # Logging configuration
|       └── schema.py       # Pydantic BaseModel
├── schema.py               # Pydantic models
└── main.py                 # Example usage
```

## Features

- Asynchronous HTTP client with session management
- Concurrent request handling
- Structured logging with rotation
- Pydantic models for response validation
- Custom headers and proxy support
- Error handling and logging

## Usage

```python
import json
import asyncio
from aio_http.core.base import AioHttpClientManager
from aio_http.core.logger import logger

from schema import Joke


async def main() -> None:
    """
        Main async function that demonstrates making multiple concurrent HTTP requests to the JokeAPI.
        It uses AioHttpClientManager to handle async HTTP requests with custom headers.
        The function fetches multiple jokes, processes the responses, and prints them.
        
        Returns:
            None
        
        Raises:
            Exception: If there's an error during the HTTP requests or response processing
        """
    
    client_manager = AioHttpClientManager(async_mode=True)

    custom_headers = {
        "Authorization": "Bearer YOUR_TOKEN_HERE",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    client_manager.set_headers(custom_headers)

    urls = [
        "https://v2.jokeapi.dev/joke/Any",
        "https://v2.jokeapi.dev/joke/Any",
        "https://v2.jokeapi.dev/joke/Any",
        "https://v2.jokeapi.dev/joke/Any",
        "https://v2.jokeapi.dev/joke/Any",
        "https://v2.jokeapi.dev/joke/Any",
    ]

    try:
        responses = await client_manager.async_multi_request("GET", urls)
        for url, response in zip(urls, responses):
            if isinstance(response, Exception):
                logger.error("Failed to get response for %s: %s", url, response)
            else:
                joke = json.loads(response)
                response = Joke.parse_obj(joke)
                print(f"Response from {url}:", response)

    except (Exception, pydantic.ValidationError) as e:
        logger.error("An error occurred: %s", e)
        
    finally:
        await client_manager.close()


if __name__ == "__main__":
    asyncio.run(main())
```

## Components

### AioHttpClientManager (base.py)
- Manages aiohttp sessions
- Handles async requests
- Supports custom headers and proxies
- Includes error handling and logging

### Logger (logger.py)
- Configurable logging levels
- File rotation support
- Formatted log output
- Daily log files

### Schema Models (schema.py)
- Pydantic models for data validation
- Type hints and field validation
- Custom field aliases
- Optional field support

## Requirements

- Python 3.7+
- aiohttp
- pydantic
- logging

## Rquirements Installation
```bash
pip install-r requirements.txt
```
