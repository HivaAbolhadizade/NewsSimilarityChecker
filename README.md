# Persian News Comparison Using Cosine Similarity

This project compares news articles from two Persian news websites using **Cosine Similarity** and **TF-IDF** to determine if the articles are duplicates or not.

## How It Works

1. The script fetches the latest article from two news websites using the provided CSS selectors.
2. After fetching the article text, **Hazm** is used to preprocess the Persian text by:
   - Normalizing the text.
   - Tokenizing the words.
   - Removing stop words.
   - Applying stemming/lemmatization.
3. The processed articles are then compared using **TF-IDF** and **Cosine Similarity**.
4. If the similarity score exceeds the set threshold (e.g., 0.9), the articles are considered duplicates. Otherwise, both articles are printed.

## Prerequisites

Ensure you have the following Python libraries installed:

```bash
pip install requests beautifulsoup4 hazm scikit-learn
```

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   ```
2. Navigate to the project directory
    ```bash
    cd NewsSimilarityChecker
```
3. Run the script:
   ```bash
   News_Similarity_Checker_app.py
   ```
## Customization
. Threshold: You can adjust the similarity threshold in the script to determine how similar the articles must be to be considered duplicates.
. CSS Selectors: Modify the link_selector and article_text_selector variables in the script based on the HTML structure of the news websites you're scraping.
   
