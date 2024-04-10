import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import pickle

# Read the normalized corpus
df = pd.read_csv("NLP_functions/Corpus.csv")
element = df['Contenido']

#Create regex for count_vectorized
regex = r'[\w.]+-?%?\w*|\w+\n|\.|\¿|\?|:|\¡|\!|\,|\;'

#----------------------Binary-----------------------

class binary_content:
    
    def __init__(self) -> None:
        # This object has the vocabulary of the the title + content, so we can just use .transform()
        self.unigramVocabulary = CountVectorizer(binary=True, token_pattern=regex).fit(element)
        self.bigramVocabulary = CountVectorizer(binary=True, token_pattern=regex, ngram_range=(2,2)).fit(element)
    
    
    def unigram_matrix(self):
        if (os.path.exists('NLP_functions/pickles_files/content_binary_unigram_matrix.pkl')):
            with open ('NLP_functions/pickles_files/content_binary_unigram_matrix.pkl','rb') as pkl_file:
                unigramMatrix = pickle.load(pkl_file)
        else:
            with open ('NLP_functions/pickles_files/content_binary_unigram_matrix.pkl','wb') as pkl_file:
                unigramMatrix = self.unigramVocabulary.transform(element)
                pickle.dump(unigramMatrix, pkl_file)                
        return unigramMatrix.toarray()
        
        
    def bigram_matrix(self):
        if (os.path.exists('NLP_functions/pickles_files/content_binary_bigram_matrix.pkl')):
            with open ('NLP_functions/pickles_files/content_binary_bigram_matrix.pkl','rb') as pkl_file:
                bigramMatrix = pickle.load(pkl_file)
        else:
            with open ('NLP_functions/pickles_files/content_binary_bigram_matrix.pkl','wb') as pkl_file:
                bigramMatrix = self.bigramVocabulary.transform(element)
                pickle.dump(bigramMatrix, pkl_file)        
        return bigramMatrix.toarray()

# --------------------------Frequency-----------------------    
    
class frequency_content:
    
    def __init__(self) -> None:
        self.unigramVocabulary = CountVectorizer(token_pattern=regex).fit(element)
        self.bigramVocabulary = CountVectorizer(token_pattern=regex, ngram_range=(2,2)).fit(element)
    
    
    def unigram_matrix(self):
        if (os.path.exists('NLP_functions/pickles_files/content_frequency_unigram_matrix.pkl')):
            with open ('NLP_functions/pickles_files/content_frequency_unigram_matrix.pkl','rb') as pkl_file:
                unigramMatrix = pickle.load(pkl_file)
        else:
            with open ('NLP_functions/pickles_files/content_frequency_unigram_matrix.pkl','wb') as pkl_file:
                unigramMatrix = self.unigramVocabulary.transform(element)
                pickle.dump(unigramMatrix, pkl_file)
        return unigramMatrix.toarray()
        
        
    def bigram_matrix(self):
        if (os.path.exists('NLP_functions/pickles_files/content_frequency_bigram_matrix.pkl')):
            with open ('NLP_functions/pickles_files/content_frequency_bigram_matrix.pkl','rb') as pkl_file:
                bigramMatrix = pickle.load(pkl_file)
        else:
            with open ('NLP_functions/pickles_files/content_frequency_bigram_matrix.pkl','wb') as pkl_file:
                bigramMatrix = self.bigramVocabulary.transform(element)
                pickle.dump(bigramMatrix, pkl_file)    
        return bigramMatrix.toarray()
    
# -------------------Tf-idf----------------------

class tfidf_content:
    
    def __init__(self) -> None:
        self.unigramVocabulary = TfidfVectorizer(token_pattern=regex).fit(element)
        self.bigramVocabulary = TfidfVectorizer(token_pattern=regex, ngram_range=(2,2)).fit(element)
        
    def unigram_matrix(self):
        if (os.path.exists('NLP_functions/pickles_files/content_tfidf_unigram_matrix.pkl')):
            with open ('NLP_functions/pickles_files/content_tfidf_unigram_matrix.pkl','rb') as pkl_file:
                unigramMatrix = pickle.load(pkl_file)
        else:
            with open ('NLP_functions/pickles_files/content_tfidf_unigram_matrix.pkl','wb') as pkl_file:
                unigramMatrix = self.unigramVocabulary.transform(element)
                pickle.dump(unigramMatrix, pkl_file)
        return unigramMatrix.toarray()
        
        
    def bigram_matrix(self):
        if (os.path.exists('NLP_functions/pickles_files/content_tfidf_bigram_matrix.pkl')):
            with open ('NLP_functions/pickles_files/content_tfidf_bigram_matrix.pkl','rb') as pkl_file:
                bigramMatrix = pickle.load(pkl_file)
        else:
            with open ('NLP_functions/pickles_files/content_tfidf_bigram_matrix.pkl','wb') as pkl_file:
                bigramMatrix = self.bigramVocabulary.transform(element)
                pickle.dump(bigramMatrix, pkl_file)    
        return bigramMatrix.toarray()