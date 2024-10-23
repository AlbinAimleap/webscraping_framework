import json
import asyncio
from tlsclient.core.base import HTTPClient
from tlsclient.core.logger import logger

from schema import Joke

async def main() -> None:
    """
        Main async function that demonstrates making multiple concurrent HTTP requests to the JokeAPI.
        It creates an HTTP client, sets headers, makes parallel requests to fetch jokes,
        and parses the responses into Joke objects.
        
        Returns:
            None
        
        Raises:
            Exception: If any error occurs during the HTTP requests or response processing
        """
    
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
            response  = json.loads(response.text)
            joke = Joke.parse_obj(response)
            print(f"Response {i + 1}:", joke)

    except (json.JSONDecodeError, Exception) as e:
        logger.error("An error occurred: %s", e)
        
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
