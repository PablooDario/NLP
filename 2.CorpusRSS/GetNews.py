import feedparser
from csv import DictWriter
import pandas as pd
import stanza

def main():
    # Setup stanza in spanish
    stanza.download ('es')
    # Global raw DataFrame
    global raw_df 
    raw_df = pd.read_csv("/Users/k-dot/Documents/NLP/2.CorpusRSS/raw_data_corpus.csv")
    # Global Normalized Dataframe
    global normalized_df
    normalized_df = pd.read_csv("/Users/k-dot/Documents/NLP/2.CorpusRSS/normalized_data_corpus.csv")
    # Global Field_names for CSV
    global field_names 
    field_names = ["Source", "Title", "Content", "Section", "URL", "Date"]
    # Global Stop Words for the normalization process
    global stop_words
    stop_words = ['DET', 'ADP', 'CCONJ', 'SCONJ', 'PRON']
    # Variable for NLP process
    global nlp
    nlp = stanza.Pipeline('es')
    
    # Add the news of La Jornada an Expansion 
    La_Jornada()
    Expansion()
    
    
def normalize_data(entry: str) -> str:
    # Normalize the content (Tokenization, Stop Words, Lemmatization)
        doc = nlp(entry)
        content = ''
        for sent in doc.sentences:
            for token in sent.words:
                # If the word is a stop word do not add it to the content string
                if token.pos in stop_words:
                    continue
                content += ' ' + token.lemma
        # If the content is string type and the it is not null, capitalize the first word
        if isinstance(content, str) and len(content) > 0:
            content = content.lstrip()
            content = content[0].upper() + content[1:]
        return content
            

def write_raw_data_corpus(source, section, feed):
    # Open CSV file
    with open("/Users/k-dot/Documents/NLP/2.CorpusRSS/raw_data_corpus.csv", mode='a', newline='', encoding='utf-8') as csv_file:
        writer = DictWriter(csv_file, field_names)
        # Check every New
        for entry in feed.entries:
            if entry.title in raw_df['Title'].values:
                continue
            # give format to the date
            published_date = entry.published_parsed
            date = f"{published_date.tm_mday}/{published_date.tm_mon}/{published_date.tm_year}"
            # Append the new
            writer.writerow({"Source": source, "Title": entry.title, "Content": entry.description, "Section": section, "URL": entry.link, 'Date': date})
            
            
def write_normalized_data(source, section, feed):
    #Open CSV file
    with open("/Users/k-dot/Documents/NLP/2.CorpusRSS/normalized_data_corpus.csv", mode='a', newline='', encoding='utf-8') as csv_file:
        writer = DictWriter(csv_file, field_names)
        # Check every new
        for entry in feed.entries:
            #Normalize title
            title = normalize_data(entry.title)
            if title in normalized_df['Title'].values:
                continue
            # Give format to the date
            published_date = entry.published_parsed
            date = f"{published_date.tm_mday}/{published_date.tm_mon}/{published_date.tm_year}"
            # Normalize the title
            content = normalize_data(entry.description)
            
            writer.writerow({"Source": source, "Title": title, "Content": content, "Section": section, "URL": entry.link, 'Date': date})
        
            
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
        write_raw_data_corpus("La Jornada", sections[section], feed)
        #Add Normalized Data
        write_normalized_data("La Jornada", sections[section], feed)

        
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
        write_raw_data_corpus("Expansión", sections[section], feed)
        #Add Normalized Data
        write_normalized_data("Expansión", sections[section], feed)
        
        
if __name__ == "__main__":
    main()