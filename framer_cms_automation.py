import json
import os
import requests
import csv
from g4f.client import Client
from together import Together
import time

client = Together(api_key="8a4175271079b2200c7dbdfdc833799e12d2022581fbe546f93d5976c4ca650e")
gpt4free_client = Client()


def read_csv(filename):
    with open(filename, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        # Skip header row if it exists
        header = next(csv_reader)
        data = list(csv_reader)
    return header, data

def write_csv(filename, header, data):
    with open(filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)  # Write header
        csv_writer.writerows(data)  
        
    
def generate_blog_post_content(topic):
    response = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
        messages=[
            {"role": "user", "content": f"Write a comprehensive blog post about: {topic}. Only return the content and nothing else."}
            ]
    )
    print("Blog post generated: ", response.choices[0].message.content)
    return response.choices[0].message.content + "If you're looking for a powerful, student-friendly note-taking app, look no further than **Oneboard**. Designed to enhance your learning experience, Oneboard offers seamless handwriting and typing capabilities, intuitive organization features, and advanced tools to boost productivity. Whether you're annotating PDFs, organizing class notes, or brainstorming ideas, Oneboard simplifies it all with its user-focused design. Experience the best of digital note-taking and make your study sessions more effective with Oneboard. [Download Oneboard on the App Store](https://apps.apple.com/app/oneboard)."

def generate_blog_post_image(topic):
    image_prompt = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
        messages=[
            {"role": "system", "content": "You are a large language model designed to generate detailed, visually captivating image prompts for blog post covers. Given the theme of a blog post, create an image prompt that aligns perfectly with the content and conveys the central message. Be clear, specific, and descriptive, including elements like style, color scheme, and composition. Ensure that the prompt is concise yet sufficient for creating an appealing and theme-relevant image. Only return the image prompt and nothing else."},
            {"role": "user", "content": f"Generate a detailed image prompt for a blog post about: {topic}."}
            ]
    )
    print("Image prompt generated: ", image_prompt.choices[0].message.content)
    
    image_completion = client.images.generate(
        prompt=image_prompt.choices[0].message.content,
        model="black-forest-labs/FLUX.1-schnell-Free",
        steps=1
    )
    
    return image_completion.data[0].url

def generate_page_description(topic):
    response = gpt4free_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Generate a seo-friendly page description for a blog post about: {topic}. Only return the page description and nothing else."}]
    )
    return response.choices[0].message.content

def generate_blog_posts(topics):
    
    csv_header = ["title", "author", "cover_description", "content", "cover_image_url", "page_description"]
    blog_data = []
    
    for topic in topics:
        title = topic
        author = "Timon Harz"
        output_filename = "data/blog_posts.csv"

        
        try:
            content = generate_blog_post_content(topic)
            cover_image_url = generate_blog_post_image(topic)
            page_description = generate_page_description(topic)
            
            with open(output_filename, 'a', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([title, author, cover_image_url, content, cover_image_url, page_description])
            
            print(f"Successfully generated and saved blog post for topic: {topic}")
                        
        except Exception as e:
            print(f"Error generating blog post for topic {topic}: {e}")
            continue
        
    print(f"Blog posts generated and saved to {output_filename}")
        
    
    
def generate_blog_post_themes():
    response = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
        messages=[
            {"role": "system", "content": "You are a blog theme generator. Generate an array of blog post themes related to productivity, AI, note-taking, and student life. Return only a JSON array of strings."},
            {"role": "user", "content": "Generate 50 blog post themes"}
        ]
    )
    
    try:
        print("Response: ", response.choices[0].message.content)
        # Parse the response content as JSON
        extracted_json = extract_json_content(response.choices[0].message.content)
        print("Generated themes: ", extract_json_content)
        return extract_json_content
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def extract_json_content(text):
    try:
        # For JSON arrays
        if '[' in text and ']' in text:
            start = text.find('[')
            end = text.rfind(']') + 1
            json_str = text[start:end]
            return json.loads(json_str)
        
        # For JSON objects
        elif '{' in text and '}' in text:
            start = text.find('{')
            end = text.rfind('}') + 1
            json_str = text[start:end]
            return json.loads(json_str)
            
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

if __name__ == "__main__":
    while True:
        try:
            # Generate new themes
            print("Generating new blog post themes...")
            themes = generate_blog_post_themes()
            
            if not themes:
                print("No themes were generated. Retrying in 60 seconds...")
                time.sleep(60)
                continue
                
            # Generate blog posts for each theme
            print(f"Generating blog posts for {len(themes)} themes...")
            generate_blog_posts(themes)
            
            # Add a delay before starting the next cycle
            print("Completed cycle. Waiting 5 minutes before starting next cycle...")
            time.sleep(60)
            
        except Exception as e:
            print(f"An error occurred in the main loop: {e}")
            print("Waiting 60 seconds before retrying...")
            time.sleep(60)
