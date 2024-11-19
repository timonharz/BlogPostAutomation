import requests
from bs4 import BeautifulSoup
import urllib.parse

def fetch_first_image(query: str) -> str:
    """
    Fetches the first image URL for a given query from Google Image Search.

    Args:
        query (str): The search query for the image.

    Returns:
        str: The URL of the first image result, or a message if no image is found.
    """
    # Convert the query into a format suitable for a URL
    search_url = "https://www.google.com/search"
    params = {
        "q": query,
        "tbm": "isch",  # Image search
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the first image element
        img_tag = soup.find("img")
        print("Images: ", img_tag)
        if img_tag and img_tag.get("src"):
            return img_tag["src"]
        else:
            return "No image found for the query."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Example usage
if __name__ == "__main__":
    query = "beautiful landscapes"
    image_url = fetch_first_image(query)
    print("First image URL:", image_url)