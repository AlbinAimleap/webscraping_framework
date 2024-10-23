
# TLS Client Example Project

This project demonstrates a TLS client implementation using `tls-client` with structured logging and Pydantic models.

## Project Structure

```
tls_client_example/
├── tlsclient/
│   └── core/
│       ├── base.py         # TLSClientManager and HTTPClient implementation
│       ├── logger.py       # Logging configuration
│       └── schema.py       # Pydantic BaseModel
├── schema.py               # Pydantic models
└── main.py                 # Example usage
```

## Features

- TLS client with session management
- Concurrent request handling
- Structured logging with rotation
- Pydantic models for response validation
- Custom headers and proxy support
- Error handling and logging

## Usage

```python
import json
import asyncio
from tlsclient.core.base import HTTPClient
from tlsclient.core.logger import logger

from schema import Joke

async def main() -> None:
    client = HTTPClient(async_mode=True)
    
    headers = {
        "Authorization": "Bearer YOUR_TOKEN_HERE",
        "Content-Type": "application/json"
    }
    client.set_headers(headers)

    try:
        urls = [
            "https://v2.jokeapi.dev/joke/Any",
            "https://v2.jokeapi.dev/joke/Any",
            "https://v2.jokeapi.dev/joke/Any",
            "https://v2.jokeapi.dev/joke/Any",
            "https://v2.jokeapi.dev/joke/Any",
            "https://v2.jokeapi.dev/joke/Any",
        ]
        
        responses = await client.async_multi_request(urls, "GET")
        for i, response in enumerate(responses):
            response = json.loads(response.text)
            joke = Joke.parse_obj(response)
            print(f"Response {i + 1}:", joke)

    except (json.JSONDecodeError, Exception) as e:
        logger.error("An error occurred: %s", e)
        
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Components

### TLSClientManager and HTTPClient (base.py)
- Manages TLS client sessions
- Handles both sync and async requests
- Supports custom headers and proxies
- Includes error handling and logging
- Concurrent request support

### Logger (logger.py)
- Configurable logging levels
- File rotation support with TimedRotatingFileHandler
- Formatted log output
- Daily log files with backup count

### Schema Models (schema.py)
- Pydantic models for data validation
- Type hints and field validation
- Custom field aliases
- Optional field support
- Flags model for joke attributes

## Requirements

- Python 3.7+
- tls-client
- pydantic
- logging

## Requirements Installation
```bash
pip install -r requirements.txt
```
