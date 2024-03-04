import feedparser
from csv import DictWriter
import pandas as pd
import stanza

def main():
    #Setup stanza in spanish
    stanza.download ('es')
    
    global raw_df 
    raw_df = pd.read_csv("raw_data.csv")
    
    global normalized_df
    normalized_df = pd.read_csv("normalized_data_corpus.csv")
    
    global field_names 
    field_names = ["Source", "Title", "Content", "Section", "URL", "Date"]
    
    global stop_words
    stop_words = ['DET', 'ADP', 'CCONJ', 'SCONJ', 'PRON']
    
    La_Jornada()
    Expansion()


def write_raw_data(source, section, feed):
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
            
def normalize_data(source, section, feed):
    nlp = stanza.Pipeline('es')
                
    with open("normalized_data_corpus.csv", mode='a', newline='', encoding='utf-8') as csv_file:
        writer = DictWriter(csv_file, field_names)
        # Append every entry in a row
        for entry in feed.entries:
            if entry.title in normalized_df['Title'].values:
                continue
            # give format to the date
            published_date = entry.published_parsed
            date = f"{published_date.tm_mday}/{published_date.tm_mon}/{published_date.tm_year}"
            # Normalize content
            doc = nlp(entry.description)
            content = ''
            for sent in doc.sentences:
                for token in sent.words:
                    if token.pos in stop_words:
                        continue
                    content += ' ' + token.lemma
            
            writer.writerow({"Source": source, "Title": entry.title, "Content": content, "Section": section, "URL": entry.link, 'Date': date})
            
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
        #Fetch rss data
        feed = feedparser.parse(Jornada_URL1+section+Jornada_URL2)
        #Write the whole new in the Raw Corpus
        write_raw_data("La Jornada", sections[section], feed)
        #Add Normalized Data
        normalize_data("La Jornada", sections[section], feed)

        
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
        #Fetch rss data
        feed = feedparser.parse(Expansion_URL+section)
        #Write the whole new in the Raw Corpus
        write_raw_data("Expansión", sections[section], feed)
        normalize_data("Expansión", sections[section], feed)
        
if __name__ == "__main__":
    main()