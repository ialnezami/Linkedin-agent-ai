import ollama
import random
import json
import os

# Define the path for the JSON file to store post history
POST_HISTORY_FILE = 'post_history.json'

class LinkedInManager:
    def __init__(self):
        self.post_history = self.load_post_history()
        self.domains = [
            'Web Development(design pattern ts)', 'Data Science', 'Cloud Computing',
            'Machine Learning', 'DevOps', 'Blockchain', 'Cybersecurity',
            'Artificial Intelligence', 'Internet of Things', 'Quantum Computing',
            'AWS', 'Azure', 'Google Cloud', 'design pattern'
        ]

    def load_post_history(self):
        """Load the post history from a JSON file."""
        if os.path.exists(POST_HISTORY_FILE):
            with open(POST_HISTORY_FILE, 'r') as file:
                return set(json.load(file))  # Load history and convert it to a set
        return set()  # Return an empty set if the file does not exist

    def save_post_history(self):
        """Save the post history to a JSON file."""
        with open(POST_HISTORY_FILE, 'w') as file:
            json.dump(list(self.post_history), file)  # Convert set back to list for JSON serialization

    def generate_post(self, domain):
        """Generate a unique LinkedIn post based on the given domain and history."""
        prompt = f"Generate a unique LinkedIn post related to {domain}. "
        prompt += "The post should not include any personal experience or opinion."
        
        messages = [{'role': 'user', 'content': prompt}]
        
        # Call the Ollama model to generate the post
        response = ollama.chat(
            model='engineer',
            messages=messages,
            tools=None,
        )
        
        new_post = response['message']['content'].strip()
        return new_post

    def generate_comment(self, post):
        """Generate a positive and inspiring comment based on the given post content."""
        prompt = f"Generate a positive and inspiring comment based on the following LinkedIn post:\n{post}"
        messages = [{'role': 'user', 'content': prompt}]
        
        response = ollama.chat(
            model='engineer',
            messages=messages,
            tools=None,
        )
        
        new_comment = response['message']['content'].strip()
        return self.clean_linkedin_post(new_comment)

    def clean_linkedin_post(self, post):
        """Remove the first paragraph and any text after the hashtags from the LinkedIn post."""
        paragraphs = post.split('\n\n')  # Split by double newlines for paragraphs

        # Remove the first paragraph if there are multiple paragraphs
        cleaned_post = '\n\n'.join(paragraphs[1:]) if len(paragraphs) > 1 else post

        # Trim content from the first hashtag onward
        hashtag_index = cleaned_post.find('#')
        if hashtag_index != -1:
            cleaned_post = cleaned_post[:hashtag_index].strip()
        prompt ="clean this post please"
        # expertLinkedin:latest 
        messages = [{'role': 'user', 'content': prompt+":"+cleaned_post}] 
        cleaned_post = ollama.chat(
            model='expertLinkedin',
            messages=messages,
            tools=None,
        )    
        return cleaned_post

    def post_to_linkedin(self, domain):
        """Generate a new LinkedIn post, ensuring it's unique."""
        new_post = self.generate_post(domain)
        
        # Check if the generated post is unique
        while new_post in self.post_history:
            print("Duplicate post detected. Generating a new one...")
            new_post = self.generate_post(domain)
        
        # Add the new post to history and save it
        self.post_history.add(new_post)
        self.save_post_history()
        
        return new_post  # Return for posting to LinkedIn

    def generate_new_post(self, domain):
        """Generate a new post by randomly selecting a domain and ensuring uniqueness."""
        if domain:
            return self.post_to_linkedin(domain)
        else:
            domain = random.choice(self.domains)  # Randomly select a domain
            return self.post_to_linkedin(domain)

