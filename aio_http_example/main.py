import json
import asyncio
from pydantic import ValidationError
from aio_http.core.base import AioHttpClientManager
from aio_http.core.logger import logger
from aio_http.core.db import init_db, SessionLocal
from icecream import ic

from schema import Joke, Flags

# Initialize the database
init_db()

async def fetch_jokes(client_manager: AioHttpClientManager, urls: list[str]) -> list[dict]:
    """
    Fetch multiple jokes concurrently from the given URLs.
    
    Args:
        client_manager (AioHttpClientManager): The client manager for making requests.
        urls (list[str]): A list of URLs to fetch jokes from.
    
    Returns:
        list[dict]: A list of jokes fetched from the URLs.
    """
    responses = await client_manager.multi_request(urls)  # Use multi_request instead of request
    jokes = []

    for url, response in zip(urls, responses):
        if isinstance(response, Exception):
            logger.error("Failed to get response for %s: %s", url, response)
        else:
            try:
                joke_data = json.loads(response)
                jokes.append(joke_data)
            except json.JSONDecodeError as e:
                logger.error("Failed to parse JSON response from %s: %s", url, e)

    return jokes


def save_jokes(jokes: list[dict]) -> None:
    """
    Process the fetched jokes and save them to the database.
    
    Args:
        jokes (list[dict]): A list of jokes to process.
    
    Returns:
        None
    """
    try:        
        for joke in jokes:
            flags_data = joke.get("flags", {})
            flags = Flags(**flags_data)
            flags_id = flags.save()
            
            joke_model = Joke(
                error=joke.get("error", False),
                category=joke.get("category", ""),
                joke_type=joke.get("type"),
                joke=joke.get("joke"),
                setup=joke.get("setup"),
                delivery=joke.get("delivery"),
                safe=joke.get("safe", True),
                lang=joke.get("lang", ""),
                flags=flags_id
            )

            joke_model.save()
            
            logger.info(f"Joke saved successfully")
 
    except Exception as e:
        logger.error("An error occurred while saving jokes: %s", e)


async def main() -> None:
    """
    Main async function that fetches and processes jokes from JokeAPI.
    
    Returns:
        None
    """
    async with AioHttpClientManager() as client_manager:  # Use async context manager for client manager
        custom_headers = {
            "Authorization": "Bearer YOUR_TOKEN_HERE",  # Ensure to replace with your token
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
        client_manager.set_headers(custom_headers)

        urls = ["https://v2.jokeapi.dev/joke/Any"] * 10
        try:
            jokes = await fetch_jokes(client_manager, urls)
            save_jokes(jokes) 
        except (Exception, ValidationError) as e:
            logger.error("An error occurred: %s", e)

if __name__ == "__main__":
    asyncio.run(main())
