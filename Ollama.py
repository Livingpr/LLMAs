from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import subprocess
import json

app = Flask(__name__)

# Function to fetch and parse content from a website
def fetch_website_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

# Function to query Ollama with the RAG model
def query_ollama(prompt):
    result = subprocess.run(
        ['ollama', 'run', 'llama2', prompt],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    # url = data.get('url')
    url = 'https://www.bbc.com/news/articles/c3wp4qnljd1o'
    question = data.get('question')

    if not url or not question:
        return jsonify({'error': 'URL and question are required'}), 400

    # Fetch content from the specified URL
    website_content = fetch_website_content(url)

    # Combine the website content with the user question
    prompt = f"Based on the following content:\n\n{website_content}\n\nAnswer the question: {question}"

    # Get the response from Ollama
    response = query_ollama(prompt)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)