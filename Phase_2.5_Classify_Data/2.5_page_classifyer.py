import logging
import requests
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

class WebsiteClassifier:
    def __init__(self, model_name, tokenizer_name, white_list_categories):
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.white_list_categories = set(white_list_categories)
        self.tfidf_vectorizer = TfidfVectorizer()

    def classify(self, text):
        # Encode the text using the tokenizer
        encoded_text = self.tokenizer(text, truncation=True, padding=True, return_tensors="pt")

        # Make a prediction using the model
        prediction = self.model(encoded_text)

        # Get the predicted category
        predicted_category = prediction.logits.argmax(-1).item()

        # Get the probability of the predicted category
        predicted_category_probability = prediction.logits[0, predicted_category].item()

        return predicted_category, predicted_category_probability

    def match_synonyms(self, category, text):
        # Get the TF-IDF vectors of the category and the text
        category_tfidf_vector = self.tfidf_vectorizer.transform([category])
        text_tfidf_vector = self.tfidf_vectorizer.transform([text])

        # Calculate the cosine similarity between the two vectors
        cosine_similarity = category_tfidf_vector.dot(text_tfidf_vector.T)[0][0]

        # Return True if the cosine similarity is greater than a threshold, False otherwise
        return cosine_similarity > 0.5

    def is_page_relevant(self, url, category):
        # Get the page content
        response = requests.get(url)
        page_content = response.content.decode()

        # Classify the page content
        predicted_category, predicted_category_probability = self.classify(page_content)

        # Check if the predicted category is in the white list and the probability is greater than a threshold
        return predicted_category in self.white_list_categories and predicted_category_probability > 0.5

    def get_page_summary(self, url):
        # Get the page content
        response = requests.get(url)
        page_content = response.content.decode()

        # Extract the summary of the page content
        summary = page_content[:100]

        return summary

    def log_page(self, url, category, summary):
        # Log the page URL, category, and summary to a file
        with open("output.txt", "a") as f:
            f.write(f"{url}, {category}, {summary}\n")

def main():
    # Create a website classifier
    website_classifier = WebsiteClassifier(model_name="distilbert-base-uncased", tokenizer_name="distilbert-base-uncased", white_list_categories=["transport", "technology"])

    # Get the URL to classify
    url = "https://www.google.com/"

    # Classify the URL
    category, predicted_category_probability = website_classifier.classify(url)

    # If the URL is relevant to one of the white list categories, log it
    if website_classifier.is_page_relevant(url, category):
        summary = website_classifier.get_page_summary(url)
        website_classifier.log_page(url, category, summary)

if __name__ == "__main__":
    main()
