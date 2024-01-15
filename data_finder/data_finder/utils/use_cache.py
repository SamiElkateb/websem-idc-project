import json
import os


def load_cache(cache_name: str) -> dict:
    """Load data from a cache file.

    Args:
        cache_name (str): The name of the cache file.

    Returns:
        The data loaded from the cache, or None if the cache does not exist.
    """
    try:
        with open(f"./cache/{cache_name}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_cache(cache_name: str, data):
    """Save data to a cache file.

    Args:
        cache_name (str): The name of the cache file.
        data: The data to be saved in the cache.
    """
    if not (os.path.exists("cache") and os.path.isdir("cache")):
        os.makedirs("cache")
    with open(f"./cache/{cache_name}.json", "w") as file:
        json.dump(data, file)
