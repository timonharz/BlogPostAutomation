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
            
            time.sleep(11)
            
        except Exception as e:
            print(f"Error generating blog post for topic {topic}: {e}")
            continue
        
    print(f"Blog posts generated and saved to {output_filename}")
        
    
    
def generate_blog_post_themes():
    pass


generate_blog_posts(["Benefits of Digital Note-Taking", "Best AI Note-Taking Apps for Students", "AI-Powered Productivity Tools", "AI in Education", "AI Meeting Assistants for Improved Team Productivity", "Ethics of AI in Academic Settings", "How AI Enhances Personal Workflow", "Time Management Strategies for Students", "Best Practices for Digital Decluttering", "Overcoming Procrastination with Technology", "Top Apps for Workflow Automation", "Top Note-Taking Techniques for Students", "AI-Powered Study Tools", "Digital Annotation Tools for Research", "Creating a Study Plan Using AI", "Balancing Digital and Handwritten Notes", "Choosing the Right Note-Taking App for Your Learning Style", "Best Productivity Apps for Students in 2024", "Top Tools for Group Projects and Collaborative Work", "Survival Guide for First-Year University Students", "Digital Tools for Exam Preparation", "The Future of AI in Higher Education", "The Rise of Generative AI in Note-Taking", "Data Security Concerns with AI Tools", "How Remote Work is Shaping AI Development", "AI Legislation and Its Impact on Students", "How to Take Effective Notes with AI Assistance", "Innovative AI Features in Note-Taking Apps", "Maximizing Productivity with AI Meeting Assistants", "How to Use AI to Summarize Long Articles and Texts", "Personalizing Your Note-Taking with AI", "The Role of AI in Collaborative Writing and Editing", "Top AI Tools for Academic Writing and Plagiarism Detection", "Strategies for Integrating AI into Study Routines", "Leveraging AI for Research Paper Organization", "How AI Enhances Academic Group Projects", "AI Tools for Thesis and Dissertation Planning", "AI's Impact on Language Learning Apps", "Building Efficient To-Do Lists with AI", "How AI Changes the Way Students Study for Exams", "AI and Productivity: A Guide for Students", "New AI Trends in 2024 for Productivity Enthusiasts", "The Pros and Cons of Using AI for Note-Taking", "Top AI Solutions for Managing Time More Effectively", "Implementing AI in University Classrooms", "How AI Can Help Reduce Academic Stress", "AI-Powered Mind Mapping Tools for Brainstorming", "The Future of Smart Notes and Digital Organizers", "Top AI Features in Popular Note-Taking Apps", "Student Case Studies: AI-Powered Productivity Success Stories", "How AI Can Make Group Discussions More Productive", "Exploring the Use of Voice Recognition in Note-Taking", "How to Transition from Manual to AI-Assisted Note-Taking", "The Intersection of AI and Productivity Apps in 2024", "Keeping Your Notes Secure with AI: Best Practices", "Emerging AI Technologies for Academic Research", "AI's Role in Annotating and Reviewing Lecture Notes", "Using AI to Find Relevant Academic Papers and Sources", "Productivity Tips: Using AI to Boost Efficiency", "Why Students Should Embrace AI Tools for Studying", "How to Choose the Best AI-Powered Note-Taking App", "Combining Traditional Study Methods with AI", "How AI Meeting Transcripts Improve Team Collaboration", "Best AI-Powered Planners and Organizers for Students", "How AI Enhances Online Learning Experiences", "AI for Real-Time Translation in Multilingual Study Groups", "AI and the Art of Summarizing Long Books and Articles", "The Role of AI in Organizing Notes and Study Materials", "Utilizing AI to Make Lecture Capture More Effective", "Choosing the Right AI Companion for Academic Success", "Security Concerns in AI-Powered Productivity Tools", "The Best Note-Taking Strategies for Science Students", "How to Integrate AI Note-Taking with Other Study Apps", "How AI Streamlines the Process of Writing Essays", "Benefits and Limitations of Using AI for Study Notes", "Top AI Innovations in Digital Learning Platforms", "Exploring Customization Features in AI Note-Taking Tools", "Top Apps for Students to Improve Focus with AI", "Why AI-Powered Note-Taking is the Future of Studying", "How AI Can Help Structure and Format Your Notes", "The Impact of AI on Collaborative Studying", "AI Tools That Help Organize Group Projects", "AI Features That Make Note-Taking More Accessible", "The Role of AI in Preventing Plagiarism in Academic Work", "How AI Summarization Can Save Students Time", "Personalized Learning Plans Powered by AI", "Balancing AI Use and Traditional Study Habits", "How Students Are Using AI to Prepare for Presentations", "Understanding How AI Can Aid in Time Management", "The Top AI Assistants for Student Life in 2024", "AI-Powered Solutions for Class Scheduling and Task Management", "Creative Uses for AI Note-Taking Beyond the Classroom"])