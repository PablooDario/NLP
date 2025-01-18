# News RSS Corpus Generator

This Python script is designed to scrape news articles from various sections of the New York Times RSS feed, check for new articles that haven't been previously saved, and then append them to a CSV file. It helps to build a dataset of news articles in CSV format, categorizing them by section and including the title and summary for each article.

## Files in the folder:
- `news_feed_scraper.py` (the Python script)
- A `data/` folder containing the `RawNewsCorpus.csv` file, where the news data will be saved.

## Features:
1. **Scraping RSS Feeds**: 
   - The script fetches news from various sections of the New York Times using RSS feeds.
   - The sections include: Energy & Environment, Technology, Sports, Science, Health, Arts, and Economy.

2. **Prevention of Duplicate Entries**:
   - The script checks if a news article has already been added to the CSV (based on its title).
   - New, non-duplicate articles are appended to the CSV file.

3. **Saving Data to CSV**:
   - The news articles are saved in a CSV format with columns for Section, Title, and Summary.
   - The CSV file is created in the `data/` folder, and if the file already exists, new articles are appended to it.

4. **Directory Management**:
   - The script ensures that a `data/` directory exists to store the CSV file. If it doesn’t exist, the directory is created automatically.

