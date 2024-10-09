import requests
from bs4 import BeautifulSoup
from hazm import Normalizer, word_tokenize, Stemmer, Lemmatizer, stopwords_list
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
import os

# Clears the console screen (works for Windows and Unix-based systems)
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fancy loading effect
def loading_animation(message, duration=2):
    print(message, end="")
    for _ in range(duration * 2):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print("\n")

# Stylish console header
def print_header():
    clear_console()
    print("=" * 60)
    print(" " * 20 + "📰 NEWS COMPARISON APP 📰")
    print("=" * 60)
    print()

# Stylish separator
def print_separator():
    print("-" * 60)

# Prints a welcome message
def print_welcome():
    print_header()
    print("Welcome to the News Comparison App!")
    print("Fetching and comparing articles from two news sites for you.")
    print("You will get a similarity score based on the content of both articles.")
    print_separator()
    input("Press Enter to begin...")

# Prints a goodbye message
def print_goodbye():
    print_separator()
    print("Thank you for using the News Comparison App! Goodbye. 👋")
    print_separator()

# Fancy result display
def display_result(similarity, article_1_text, article_2_text, threshold=0.9):
    clear_console()
    print_header()
    print(f"Similarity Score: {similarity:.2f}\n")
    if similarity > threshold:
        print("The articles are very similar and may be duplicates.")
        print_separator()
        print("Here's the content from the first article:\n")
        print(article_1_text[:500] + "...\n")
    else:
        print("The articles are different.")
        print_separator()
        print("Here's a preview of both articles:\n")
        print("Article 1 Preview:\n")
        print(article_1_text[:500] + "...\n")
        print_separator()
        print("Article 2 Preview:\n")
        print(article_2_text[:500] + "...\n")
    print_separator()
    input("Press Enter to exit...")

# Functions to fetch and process news remain the same
def get_latest_article_link(url, link_selector):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_link = soup.select_one(link_selector)
    
    if article_link:
        article_url = article_link['href']
        if article_url.startswith('/'):
            article_url = url + article_url
        return article_url
    return None

def get_article_text(article_url, article_text_selector):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.select_one(article_text_selector)
    return article.get_text() if article else None

# Preprocessing and Cosine Similarity functions stay the same
def preprocess_persian_text(text):
    normalizer = Normalizer()
    stemmer = Stemmer()
    lemmatizer = Lemmatizer()
    stop_words = set(stopwords_list())
    
    text = normalizer.normalize(text)
    tokens = word_tokenize(text)
    cleaned_tokens = [
        lemmatizer.lemmatize(stemmer.stem(token)) 
        for token in tokens if token not in stop_words and re.match(r'^\w+$', token)
    ]
    return ' '.join(cleaned_tokens)

def compute_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return cosine_sim[0][0]

# Main function
def main():
    print_welcome()
    
    url_1 = 'https://www.asriran.com/'
    url_2 = 'https://www.tabnak.ir/'
    link_selector_1 = '.tab-pane.fade.in.active .title5'
    link_selector_2 = '.title5'
    article_text_selector_1 = '.body'
    article_text_selector_2 = '.body'

    loading_animation("Fetching the latest articles", duration=3)
    
    latest_article_link_1 = get_latest_article_link(url_1, link_selector_1)
    latest_article_link_2 = get_latest_article_link(url_2, link_selector_2)

    if latest_article_link_1 and latest_article_link_2:
        article_text_1 = get_article_text(latest_article_link_1, article_text_selector_1)
        article_text_2 = get_article_text(latest_article_link_2, article_text_selector_2)
        
        loading_animation("Processing the articles", duration=2)

        if article_text_1 and article_text_2:
            article_1_clean = preprocess_persian_text(article_text_1)
            article_2_clean = preprocess_persian_text(article_text_2)

            similarity = compute_cosine_similarity(article_1_clean, article_2_clean)
            display_result(similarity, article_text_1, article_text_2)
        else:
            print("Could not fetch article texts.")
    else:
        print("Could not fetch article links.")
    
    print_goodbye()

# Run the app
if __name__ == "__main__":
    main()
