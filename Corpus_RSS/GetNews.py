import feedparser
from csv import DictWriter
import pandas as pd

def main():
    global raw_df 
    raw_df = pd.read_csv("raw_data.csv")
    
    global field_names 
    field_names = ["Source", "Title", "Content", "Section", "URL", "Date"]
    
    La_Jornada()
    Expansion()

def write_data_csv(source, section, url):
    #Fetch rss data
    feed = feedparser.parse(url)
    # Write data in CSV file
    with open("raw_data.csv", mode='a', newline='', encoding='utf-8') as csv_file:
        writer = DictWriter(csv_file, field_names)
        # Append every entry in a row
        for entry in feed.entries:
            if entry.title in raw_df['Title'].values:
                continue
            # give format to the date
            published_date = entry.published_parsed
            date = f"{published_date.tm_mday}/{published_date.tm_mon}/{published_date.tm_year}"
            writer.writerow({"Source": source, "Title": entry.title, "Content": entry.description, "Section": section, "URL": entry.link, 'Date': date})
            
def La_Jornada():
    Jornada_URL1 = "https://www.jornada.com.mx/rss/"
    Jornada_URL2 = ".xml?v=1"

    Jornada_sections = [
        "deportes",
        "economia",
        "ciencias",
        "cultura"
    ]

    sections = {
        "deportes" : "Sports",
        "economia" : "Economy",
        "ciencias" : "Science and technology",
        "cultura" : "Culture"
    }

    for section in Jornada_sections:
        write_data_csv("La Jornada", sections[section], Jornada_URL1+section+Jornada_URL2)
        
def Expansion():
    Expansion_URL = "https://expansion.mx/rss/"

    Expansion_sections = [
        "economia",
        "tecnologia"
    ]

    sections = {
        "economia" : "Economy",
        "tecnologia" : "Science and technology",
    }

    for section in Expansion_sections:
        write_data_csv("Expansión", sections[section], Expansion_URL+section)
        
if __name__ == "__main__":
    main()