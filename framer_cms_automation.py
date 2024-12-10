import json
import os
import requests
import csv
from g4f.client import Client
from together import Together
import time
from cover_image_fetcher import get_first_pixabay_result
from perplexity import Perplexity

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

def generate_paragraph(paragraph_title, topic):
    perplexity = Perplexity()
    
    answer = perplexity.search(f"Write a paragrpah with this title: {paragraph_title} for a blog post about: {topic}.")
    
    print("Paragraph content: ", answer)

def generate_blog_post_content_v2(topic):
    pass

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
    response = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
        messages=[
            {"role": "system", "content": "Generate a concise, SEO-optimized page description for a blog post. The description should summarize the content in a clear and engaging way, highlighting the main topic and key points. It should be no longer than 160 characters, written in a way that encourages readers to click and learn more. Ensure that the tone matches the subject matter of the post and that it includes relevant keywords for search engine optimization."},
            {"role": "user", "content": f"Generate a seo optimized page description for a blog post about this topic: {topic}."}
        ]
    )
    return response.choices[0].message.content

def humanize_text(text):
    humanization_prompt = """
    You will be given a piece of text that sounds like it was generated by AI. Your task is to rewrite this text to make it sound more human-written. 

    Follow these steps: 
    1. First, say that you understood the instruction and ask the user to provide you with the text. Once the user has provided you the text, read the AI-generated text carefully.

    2. Next, rewrite the text following these guidelines:
    a) Use a conversational tone, concise language and avoid unnecessarily complex jargon. Example: "Hey friends, today I'll show you a really useful writing tip"
    b) Use short punchy sentences. Example: "And then… you enter the room. Your heart drops. The pressure is on."
    c) Use simple language. 7th grade readability or lower. Example: "Emails help businesses tell customers about their stuff."
    d) Use rhetorical fragments to improve readability. Example: “The good news? My 3-step process can be applied to any business"
    e) Use bullet points when relevant. Example: “Because anytime someone loves your product, chances are they’ll:
    * buy from you again
    * refer you to their friends"
    f) Use analogies or examples often. Example: "Creating an email course with AI is easier than stealing candies from a baby"
    g) Split up long sentences. Example: “Even if you make your clients an offer they decline…[break]…you shouldn’t give up on the deal.”
    h) Include personal anecdotes. Example: "I recently asked ChatGPT to write me…"
    i) Use bold and italic formatting to emphasize words.
    j) Do not use emojis or hashtags
    k) Avoid overly promotional words like "game-changing," "unlock," "master," "skyrocket," or "revolutionize."

    Remember, the goal is to make the text sound natural, engaging, and as if it were written by a human rather than an AI.
    """
    response = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
        messages=[
            {"role": "system", "content": humanization_prompt},
            {"role": "user", "content": f"Humanize this text: {text}"}
        ]
    )
    return response.choices[0].message.content
    

def generate_paragraphs(topic):
    response = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
        messages=[
            {"role": "system", "content": f"You are a content creation assistant. Your task is to generate an array of concise and engaging paragraph titles for a blog post based on a given theme. The titles should be informative, spark interest, and be relevant to the theme. Include common titles such as Introduction and Conclusion along with more specific subheadings that guide the reader through the post. The titles should be suitable for an audience of students. Return the result in JSON format as an array of strings."},
            {"role": "user", "content": f"""Create a list of paragraph titles for a blog post on the theme: {topic}. The titles should use natural, straightforward language, be informative, and spark interest. Aim for titles that spark interest, highlight key points, and can guide the reader through the blog post. The titles should range from general introductions to more specific subtopics, and they should be suitable for a blog post that targets readers who are students. Return the result in JSON format as an array of strings.

Example Output:

[
  "Introduction",
  "Why This Topic Matters",
  "Key Benefits of [Topic]",
  "How to Get Started",
  "Common Mistakes to Avoid",
  "Expert Tips and Advice",
  "Real-Life Examples",
  "Conclusion"
]"""}
        ]
    )
    paragraphs = extract_json_content(response.choices[0].message.content)
    
    for paragraph in paragraphs:
        print("Paragraph title: ", paragraph)
    
    return paragraphs
    
    
    
    

def generate_blog_posts(topics):
    
    csv_header = ["title", "author", "cover_description", "content", "cover_image_url", "page_description"]
    blog_data = []
    output_filename = "data/blog_posts.csv"

    
    for topic in topics:
        title = topic
        author = "Timon Harz"
        
        paragraphs = generate_paragraphs(topic)
        
        try:
            content = ""
            
            for paragraph in paragraphs:
                paragraph_content = generate_paragraph(paragraph, topic)
            
            cover_image_url = get_first_pixabay_result(topic)
            print("Cover image url: ", cover_image_url)
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
        print("Generated themes: ", extracted_json)  # Fix: print extracted_json instead of the function
        return extracted_json  # Fix: return extracted_json instead of extract_json_content
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def get_search_query(theme):
    response = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
        messages=[
            {"role": "system", "content": "You are a Google search expert. Given a specific theme, return only the optimized Google search query without any additional text or explanation."},
            {"role": "user", "content": f"Theme: {theme}. Generate an optimized Google search query based on this theme, returning only the query without any additional text."}
        ]
    )
    print("Response: ", response.choices[0].message.content)
        
    return response.choices[0].message.content


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
            print("Completed cycle. Waiting 1 minutes before starting next cycle...")
            time.sleep(5)
            
        except Exception as e:
            print(f"An error occurred in the main loop: {e}")
            print("Waiting 60 seconds before retrying...")
            time.sleep(60)
