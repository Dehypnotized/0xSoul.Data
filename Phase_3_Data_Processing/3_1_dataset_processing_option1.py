# For me this one looks preferable

import re
import requests
from transformers import AutoTokenizer

# Define a function to process a URL
def process_url(url):
  # Make a request to the URL
  response = requests.get(url)

  # Check if the request was successful
  if response.status_code == 200:
    # Extract the text from the response
    text = response.content.decode('utf-8')

    # Return the processed text
    return process_text(text)
  else:
    # Raise an exception if the request was not successful
    raise Exception('Failed to download URL: {}'.format(url))

# Define a function to process a text file
def process_text(text):
  # Remove all HTML tags from the text
  text = re.sub('<[^>]*>', '', text)

  # Split the text into sentences
  sentences = text.split('.')

  # Tokenize the sentences
  tokens = AutoTokenizer.from_pretrained('bert-base-uncased').tokenize(sentences)

  # Return the tokenized sentences
  return tokens

# Define a main function
def main():
  # Get the URL or text file path from the user
  url_or_text_file_path = input('Enter the URL or text file path: ')

  # Process the URL or text file
  processed_data = process_url(url_or_text_file_path) if url_or_text_file_path.startswith('http://') or url_or_text_file_path.startswith('https://') else process_text(url_or_text_file_path)

  # Save the processed data to a file
  with open('processed_data.txt', 'w', encoding='utf-8') as f:
    for sentence in processed_data:
      f.write(sentence + '\n')

if __name__ == '__main__':
  main()
