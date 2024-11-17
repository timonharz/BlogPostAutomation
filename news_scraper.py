import os
import csv
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import json

def fetch_and_decode_latest_news():
    # Fetches the latest news from newsdata.io
    # Then saves the articles in a json file under /data/news/latest.json
    # Suited for the catery 'latest'
    url = "https://newsdata.io/api/1/latest"
    params = {
        'apikey': 'pub_59529b1f442d520d609626be4e9dc6340b23d',
        'country': "us"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        # Check if the status is success
        if data['status'] == 'success':
            print(f"Total Results: {data['totalResults']}")
            
            articles = []  # List to store article details
            
            articles_category = 'latest'
            
            # Iterate over each article in the results
            for article in data.get('results', []):
                title = article.get('title', 'No title available')
                link = article.get('link', 'No link available')
                pub_date = article.get('pubDate', 'No publication date available')
                source_name = article.get('source_name', 'No source name available')
                
                # Append article details to the list
                articles.append({
                    'title': title,
                    'link': link,
                    'pub_date': pub_date,
                    'source_name': source_name,
                    'category': articles_category
                })
                
                # Print the article details
                print(f"Title: {title}")
                print(f"Link: {link}")
                print(f"Publication Date: {pub_date}")
                print(f"Source: {source_name}\n")
            
            # Ensure the directory exists
            os.makedirs('data/news', exist_ok=True)
            
            # Save articles to a JSON file
            with open('data/news/latest.json', 'w') as json_file:
                json.dump(articles, json_file, indent=4)
                
        else:
            print("Failed to fetch news data.")
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Call the function
fetch_and_decode_latest_news()

