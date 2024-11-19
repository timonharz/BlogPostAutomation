import requests
from bs4 import BeautifulSoup
import urllib.parse

pixabay_api_key = '47168176-36a390e6f94970355dd1f0b33'

def get_first_pixabay_result(query):
    """
    Fetches the first Pixabay result for a given query.

    Parameters:
        query (str): The search query.
        api_key (str): Your Pixabay API key.

    Returns:
        dict: A dictionary containing details of the first result, or None if no results found.
    """
    url = "https://pixabay.com/api/"
    params = {
        "key": pixabay_api_key,
        "q": query,
        "image_type": "photo",
        "per_page": 3  # Limit to 1 result
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()

        if data["totalHits"] > 0 and "hits" in data and len(data["hits"]) > 0:
            first_result = data["hits"][0]
            return first_result["largeImageURL"]
        else:
            return None  # No results found

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
if __name__ == '__main__':
    result = get_first_pixabay_result("Dog")
    
    print("Image url: ", image_url)