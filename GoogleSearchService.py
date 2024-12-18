# Copyright (c) 2024 The Standard News and Timon Harz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from bs4 import BeautifulSoup
import json
import pandas as pd
import requests
from search import GPTService   
import time
#from text_extract.html.trafilactura import TrafilaturaSvc
from text_extract.html.beautifulsoup_extract import BeautifulSoupSvc
from bs4 import BeautifulSoup, SoupStrainer
from concurrent.futures import ThreadPoolExecutor
from lxml import html
import re
from search import SearchErrors
#import googlesearch
from time import sleep
import concurrent.futures
import os


GOOGLE_SEARCH_API_KEY = "AIzaSyArV1Wpr69KhpWMIG14eSPaaTk7a7z4-1Q"
SEARCH_ENGINE_ID = '17607ca6a871d4be5'

class GoogleSearchService:
    def __init__(self):
        pass

    #Perform Google search on one thread only
    def perform_google_search(self, query, num_results=5):
        
        start_time = time.time()  # Record the start time

        url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_SEARCH_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
        
        response = requests.get(url)
        
        data = json.loads(response.text)
        
        final_results = []
        
        if 'error' in data:
            print("Error:", data['error']['message'])
            return
        elif 'items' not in data:
            print("No search results")
            return
        else:
            search_results = data['items']
            
            limited_results = search_results[:3]
            
            num_of_results = len(limited_results)
            
            print("Total number of results: ", num_of_results)
            
            for result in limited_results:
                print("Extracting text content")
                text_content = self.extract_paragraphs(result['link'])
                final_results.append({ 
                                        "title": result['title'],
                                        "url": result['link'],
                                        "description": result['snippet'],
                                        "text": text_content
                                      })
                
        
        end_time = time.time()  # Record the end time
        execution_time = end_time - start_time  # Calculate the execution time
        print(f"Execution time: {execution_time} seconds")
        
        return final_results
        
    """
    Performs a Google search using multiple threads to fetch and process search results.

    This method sends a request to the Google Custom Search JSON API with the specified query,
    then processes a specified number of search results in parallel, extracting text content from each result's link.

    Args:
        query (str): The search query string.
        num_results (int): The number of search results to process.

    Returns:
        list: A list of dictionaries, each containing the title, URL, description, and extracted text content of a search result.

    Raises:
        Exception: If an error occurs during the fetching of text content for any search result.

    Note:
        - The method prints the total number of search results found, the execution time, and any errors encountered.
        - If the Google API returns an error or no search results, the method will print an error message and return None.
    """
    def perform_google_search_multithread(self, query, num_results):
        start_time = time.time()  # Record the start time

        url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_SEARCH_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
        
        response = requests.get(url)
        
        data = json.loads(response.text)
        
        final_results = []
        
        if 'error' in data:
            print("Error:", data['error']['message'])
            return
        elif 'items' not in data:
            print("No search results")
            return
        else:
            search_results = data['items']
            
            print(f'Unformatted search results: {search_results}')
            
            limited_results = search_results[:num_results]
            
            num_of_results = len(limited_results)
            
            print("Total number of results: ", len(search_results))
            
            def fetch_text_content(result):
                print(f"Extracting text content for URL: {result['link']}")
                text_content = self.extract_paragraphs(result['link'])
                
                if text_content is None:
                    return 
                
                return {
                    "title": result['title'],
                    "url": result['link'],
                    "description": result['snippet'],
                    "text": text_content
                }

            with ThreadPoolExecutor() as executor:
                future_to_result = {executor.submit(fetch_text_content, result): result for result in limited_results}
                for future in future_to_result:
                    try:
                        final_results.append(future.result())
                    except Exception as exc:
                        print(f"Generated an exception: {exc}")

        end_time = time.time()  # Record the end time
        execution_time = end_time - start_time  # Calculate the execution time
        print(f"Execution time: {execution_time} seconds")
        
        return final_results
    
    def search_request(self, query, num_results=10, lang='en', advanced=True, sleep_interval=0):
        try:
            results = googlesearch.search(query)
            
            print(f"Got results from google: {results}")
            search_results = []
            
            limited_results = results[:num_results]
            
            for result in limited_results:
                
                text_content = self.extract_sentences_from_url_v2(result.link)
                print("result: ", result)
                search_results.append({
                    "title": result.name,
                    "url": result.link,
                    "description": result.description,
                    "text": text_content
                })
            return search_results
        except Exception as e:
            print("Error making request:", e)
            #Switch to alternative here e.g Bing 
            return None

    def call_urls_and_extract_sentences(self, results):
        name_list, url_list, description_list, text_list = [], [], [], []

        for result in search_results:
            result_url = result['url']
            text_content = self.extract_sentences_from_url(result_url)
            description = result['description']

            print(f"text content: {text_content}")


            url_list.append(result_url)
            name_list.append(result_url)
            description_list.append(description)
            text_list.append(text_content)
            
            extracted_sentences = self.extract_sentences_from_url(result_url)
            
        return name_list, url_list, description_list, text_list

    def call_one_url(self, website_tuple):
        name, url, snippet, url_id = website_tuple
        logger.info(f"Processing url: {url}")
        sentences = self.extract_sentences_from_url(url)
        logger.info(f"  receive sentences: {len(sentences)}")
        return sentences, name, url, url_id, snippet

    
    def extract_sentences_from_url(self, url):
        print("exract sentences from url being called")
        # Fetch the HTML content of the page
        try:
            response = requests.get(url, timeout=1)
        except:
            raise SearchErrors.TextExtractionFromURLFailed("Text extraction failed")
            return []
        html_content = response.text

        # Use BeautifulSoup to parse the HTML and extract the text
        extract_text = BeautifulSoupSvc.extract_from_html(self,html_content)
        print(f"Google Search Service extracted this text: {extract_text} from this url: {url}")
        return extract_text
    
    def extract_sentences_from_url_v2(self, url):
        
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                strainer = SoupStrainer('p')  # Parse only 'p' tags
                soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)
                paragraphs = soup.find_all('p')
                sentences = []
                for paragraph in paragraphs:
                    sentences.extend(re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph.get_text()))
                sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
                return sentences
            else:
                print("Failed to fetch URL:", response.status_code)
                return []
        except Exception as e:
            print("Error processing URL:", e)
            return []

    def extract_sentences(self, url):
        """
        Extracts sentences from a website's HTML content.

        Args:
            url (str): The URL of the website.

        Returns:
            list: A list of sentences extracted from the website.
        """
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the text content from the HTML
            text = soup.get_text()

            # Use a regular expression to split the text into sentences
            sentences = re.split(r'[.!?]+', text)

            # Remove empty strings and leading/trailing whitespace from sentences
            sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

            return sentences

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return []
        
    def extract_paragraphs(self, url):
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all paragraph tags and extract their text
            paragraphs = [p.get_text() for p in soup.find_all('p')]

            # Join paragraphs into a single string with double newlines between paragraphs
            combined_paragraphs = "\n\n".join(paragraphs)

            return combined_paragraphs

        except requests.RequestException as e:
            print(f"An error occurred while fetching the URL: {e}")
            return
       # except requests.Req


    def count_tokens(input_string):
        # Split the string into tokens
        tokens = input_string.split()
    
        # Get the number of tokens
        num_tokens = len(tokens)
    
        return num_tokens

        

if __name__ == '__main__':
    search_service = GoogleSearchService()
        
    query = "Coffee"
    num_results = 20

    log_path = 'logs/logs.json'
        
    start_time = time.time()
    
    google_search_test = search_service.perform_google_search_multithread(query=query, num_results=num_results)
    print(f"Search results: {google_search_test}")

    with open(log_path, 'w') as file:
        json.dump(google_search_test, file, indent=4)
    