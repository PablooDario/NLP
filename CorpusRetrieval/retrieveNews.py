import csv
import feedparser
import os
import pandas as pd

def create_csv(path, url, sections):
    # Open the csv file were we are storing the news to avoid duplicate some news
    previous_news = pd.read_csv(path, encoding='cp1252')
    previous_news_title = previous_news['Title'].tolist()
    
    # create a list to append all the news
    rows = []
    
    # Fecth the news of each section
    for section in sections: 
        NewsFeed = feedparser.parse(url + section + '.xml')
        # Add a new, only if it has not been added before.
        for entry in NewsFeed.entries:
            if not entry.title in previous_news_title:
                rows.append({'Section': section, 'Title' : entry.title, 'Summary' : entry.summary.strip()})
    
    # Append all the new news
    with open(path, 'a', newline='', encoding='cp1252') as file:
        writer = csv.DictWriter(file, fieldnames=["Section", "Title", "Summary"])
        writer.writerows(rows)

def main():
    path = './data'
    # Create the data directory to store the news file
    if not os.path.isdir(path):
        os.mkdir(path)
    path =  os.path.join(path, 'RawNewsCorpus.csv')
    
    # If the file does not exists, create it and add the header
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='cp1252') as file:
            writer = csv.DictWriter(file, fieldnames=["Section", "Title", "Summary"])
            writer.writeheader()
    
    # Define the body of the url and the Sections we are interested in to fetchs the news  
    url = "https://rss.nytimes.com/services/xml/rss/nyt/"
    sections = ['EnergyEnvironment', 'Technology', 'Sports', 'Science', 'Health', 'Arts', 'Economy']

    create_csv(path, url, sections)

    news = pd.read_csv(path, encoding='cp1252')
    print(news.shape, news.head())
    
    
if __name__ == '__main__':
    main()