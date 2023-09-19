import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from typing import List, Union
import os

# Ensure NLTK tokenizer data is downloaded
nltk.download('punkt')


def extract_text_from_url(url: str) -> str:
    """
    Extract text content from a given URL using BeautifulSoup.

    Parameters:
    - url (str): The URL to extract content from.

    Returns:
    - str: Extracted textual content.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([para.text for para in paragraphs])
    return text


def extract_text_from_file(file_path: str) -> str:
    """
    Extract text content from a file.

    Parameters:
    - file_path (str): Path to the text file.

    Returns:
    - str: Extracted textual content.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def tokenize_text(text: str) -> List[str]:
    """
    Tokenize a given text.

    Parameters:
    - text (str): Text to be tokenized.

    Returns:
    - List[str]: List of tokens.
    """
    return word_tokenize(text)


def process_input_to_dataset(source: Union[str, List[str]], is_url=True) -> List[str]:
    """
    Process input (URL or file path) to a tokenized dataset.

    Parameters:
    - source (Union[str, List[str]]): The input URL or file path. Can be a list of URLs or file paths.
    - is_url (bool): Flag to indicate if the source is a URL or file path.

    Returns:
    - List[str]: Tokenized dataset.
    """
    all_tokens = []
    
    # Handle single string input or list of strings
    if not isinstance(source, list):
        source = [source]
    
    for item in source:
        if is_url:
            text = extract_text_from_url(item)
        else:
            text = extract_text_from_file(item)
        
        tokens = tokenize_text(text)
        all_tokens.extend(tokens)
    
    return all_tokens


if __name__ == "__main__":
    # Sample usage:
    # For URL:
    dataset_from_url = process_input_to_dataset("https://www.example.com")
    
    # For file:
    dataset_from_file = process_input_to_dataset("path_to_text_file.txt", is_url=False)
    
    # You can then save, further preprocess, or directly use these datasets for training.
