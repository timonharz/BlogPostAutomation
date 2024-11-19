"""
MIT License

Copyright (c) 2024 The Standard News

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
import csv
import requests
from bs4 import BeautifulSoup
import newspaper
from newspaper import Article
import json
from datetime import datetime
from nytimes_scraper.nyt_api import NytApi
from nytimes_scraper import run_scraper, scrape_month
from nytimes_scraper.articles import fetch_articles_by_month, articles_to_df
from nytimes_scraper.comments import fetch_comments, fetch_comments_by_article, comments_to_df


nytimes_api_key = 'a6AeM0I4pk9Xv4LG86sGYgJ2DkKGr3Lx'
nytimes_api = NytApi(nytimes_api_key)

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

def fetch_news_from_nytimes():
    articles = []
    
    article_df, comment_df = scrape_month(nytimes_api_key, date=datetime.now())
    
    print("Article df: ", article_df)

    return nytimes_paper.articles


if __name__ == '__main__': 
    # Call the function
    articles = fetch_news_from_nytimes()
    
    print(f"Fetched a total of {len(articles)} articles")

    for article in articles:
        print("Article: ", article)