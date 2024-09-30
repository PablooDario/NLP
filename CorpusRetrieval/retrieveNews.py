import csv
import feedparser
import os
import pandas as pd

def create_csv(path, url, sections):
    # Load existing titles
    previous_news = pd.read_csv(path, encoding='utf-8')
    previous_news_title = previous_news['Title'].tolist()
    
    rows = []
    
    # Fetch the news from each section
    for section in sections: 
        NewsFeed = feedparser.parse(url + section + '.xml')
        for entry in NewsFeed.entries:
            if entry.title not in previous_news_title:
                rows.append({'Section': section, 'Title': entry.title, 'Summary': entry.summary.strip()})
    
    # Append the new news if there are any
    if rows:
        df_new = pd.DataFrame(rows)
        # Since some news can be in different sections, we must make sure to not duplicate them
        df_new.drop_duplicates(subset=['Title'], inplace=True)
        df_new.to_csv(path, mode='a', header=False, index=False, encoding='utf-8')
        

def main():
    path = './data'
    # Create the data directory to store the news file
    if not os.path.isdir(path):
        os.mkdir(path)
    
    path = os.path.join(path, 'RawNewsCorpus.csv')
    
    # If the file does not exist, create it and add the header
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Section", "Title", "Summary"])
            writer.writeheader()
    
    # Define the URL and sections to fetch the news
    url = "https://rss.nytimes.com/services/xml/rss/nyt/"
    sections = ['EnergyEnvironment', 'Technology', 'Sports', 'Science', 'Health', 'Arts', 'Economy']

    create_csv(path, url, sections)

    news = pd.read_csv(path, encoding='utf-8')
    print(news.head(), '\n', news.shape)



if __name__ == '__main__':
    main()
