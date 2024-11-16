import json
import os
from g4f.client import Client

# Function to generate blog post
def generate_blog_post(topic):
    # Initialize the GPT-4 client
    client = Client()

    # Generate the blog post content in Markdown format
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Write a comprehensive blog post about: {topic} in Markdown format."}]
    )

    return response.choices[0].message.content

# Function to save blog post as a Markdown file
def save_blog_post(topic, content):
    # Create a folder for blog posts if it doesn't exist
    if not os.path.exists('blog_posts'):
        os.makedirs('blog_posts')

    # Prepare file name and path
    file_name = f"{topic.replace(' ', '_').lower()}.md"
    file_path = os.path.join('blog_posts', file_name)

    # Save content to a Markdown file
    with open(file_path, 'w') as md_file:
        md_file.write(content)

    print(f"Blog post saved as: {file_path}")

# Main function
def main():
    topics = [
    "Benefits of Digital Note-Taking",
    "How to be Productive: 11 Ways to Manage Tasks, Time, and Workflow",
    "Choosing the Right iPad as a Student",
    "The Best Note-Taking Strategies for Students",
    "Digital vs. Handwritten Notes: Which is More Effective?",
    "Top 5 Features to Look for in a Note-Taking App",
    "How to Organize Your Digital Notes for Maximum Efficiency",
    "The Psychology of Note-Taking: Why It Matters",
    "Tips for Using Apple Pencil Effectively in Oneboard",
    "How to Sync Your Notes Across Devices",
    "Creative Ways to Use Digital Notes Beyond Studying",
    "The Role of Color Coding in Effective Note-Taking",
    "How to Use Oneboard for Collaborative Projects",
    "Integrating Digital Notes with Task Management Tools",
    "The Impact of Digital Note-Taking on Learning Styles",
    "Best Practices for Backing Up Your Digital Notes",
    "How to Customize Your Note-Taking Experience in Oneboard",
    "The Future of Note-Taking: Trends to Watch",
    "Using Templates to Streamline Your Note-Taking Process",
    "How to Create Study Guides from Your Digital Notes",
    "Incorporating Visual Elements in Your Digital Notes",
    "The Importance of Reviewing and Revising Your Notes",
    "Using Mind Maps in Your Note-Taking Strategy",
    "How to Stay Focused While Taking Digital Notes",
    "Exploring Different Formats: Text, Audio, and Visual Notes",
    "Maximizing Efficiency with Keyboard Shortcuts in Oneboard",
    "Creating Interactive Notes with Links and Multimedia",
    "The Benefits of Digital Annotation on PDFs",
    "How to Use Digital Notes for Research and Writing",
    "Tips for Transitioning from Paper to Digital Notes",
    "The Advantages of a Note-Taking App for Exam Preparation",
    "Using Tags and Labels to Organize Your Digital Notes",
    "How to Craft a Productive Study Environment",
    "Maintaining Your Digital Note-Taking Habit",
    "Evaluating the Best Apps for Digital Note-Taking",
    "Leveraging AI Features in Note-Taking Apps",
    "How to Use Oneboard for Personal Projects and Journaling",
    "Exploring the Benefits of a Minimalist Note-Taking Approach",
    "Integrating Digital Notes into Your Daily Workflow",
    "How to Use Digital Notes for Time Management",
    "The Connection Between Note-Taking and Memory Retention",
    "Exploring Accessibility Features in Note-Taking Apps",
    "How to Use Oneboard for Professional Development",
    "The Evolution of Note-Taking: From Paper to Digital",
    "How to Share Your Digital Notes with Peers Effectively"
    ]

    for topic in topics:
        print(f"Generating blog post for: {topic}")
        content = generate_blog_post(topic)
        save_blog_post(topic, content)

if __name__ == "__main__":
    main()