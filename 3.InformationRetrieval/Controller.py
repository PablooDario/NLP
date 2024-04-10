import NLP_functions as nlp
import spacy
from spacy.lang.es.stop_words import STOP_WORDS
import math
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Create Vectorizers for title
binary_title = nlp.binary_title()
frequency_title = nlp.frequency_title()
tfidf_title = nlp.tfidf_title()

# Create Vectorizers for content
binary_content = nlp.binary_content()
frequency_content = nlp.frequency_content()
tfidf_content = nlp.tfidf_content()

# Create Vectorizers for title_content
binary_title_content = nlp.binary_title_content()
frequency_title_content = nlp.frequency_title_content()
tfidf_title_content = nlp.tfidf_title_content()

n = len(binary_title.bigram_matrix())

vector_list = [
    binary_title,         frequency_title,         tfidf_title,
    binary_content,       frequency_content,       tfidf_content,
    binary_title_content, frequency_title_content, tfidf_title_content
]

points = {
    "Title" : -4,
    "Content" : -1, 
    "Title+Content" : 2,
    
    "Unigrams" : 1,
    "Bigrams" : 1,
    
    "Binarized" : 3,
    "Frequency" : 4,
    "TF-IDF" : 5
}
class controller:
    def __init__(self):
        self.__text__ = None    
    
    def normalize_text(self, input_file):
        spacy_nlp = spacy.load('es_core_news_sm')
        with open(input_file, 'r', encoding='utf-8') as file:
            self.__text__ = file.read()
            if '\n' in self.__text__:
                self.__text__ = self.__text__.replace('\n', '')

        # Tokenize the text
        doc = spacy_nlp(self.__text__)

        # Lemmatization and Stop Words
        normalized_words = [token.lemma_ for token in doc if token.pos_ not in ['DET', 'ADP', 'CONJ', 'PRON']]

        text = ' '.join(normalized_words)
        normalized_list = [text]
        return normalized_list


    def cosine(self, v, w):
        val = sum(v[index] * w[index] for index in range(len(v)))
        sr_v = math.sqrt(sum(v_val**2 for v_val in v))
        sr_w = math.sqrt(sum(w_val**2 for w_val in w))
        res = round(val/(sr_v*sr_w),3)
        return res

    def local_test(self, ui, document):
        
        #Verify the vectorized type, features and element
        element = ui.element.get()
        vector_representation = ui.vector_representation.get()
        features = ui.features.get()
        
        #Sum all the points to select the correct vectorizer
        count = points[element] + points[vector_representation] + points[features]
        
        # Initialize the vectorixer object
        vector = vector_list[count]
        
        #Select Unigram or Bigram
        if features == "Unigrams":
            document_matrix = vector.unigramVocabulary.transform(document).toarray()
            matrix = vector.unigram_matrix()
        else:
            document_matrix = vector.bigramVocabulary.transform(document).toarray()
            matrix = vector.bigram_matrix()
        
        #Make cosine similarity
        compared_documents = {}
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            compared_documents[idx] = similarity*100
            
        compared_documents = dict(sorted(compared_documents.items(), key=lambda x:x[1], reverse=True)[:10])
        
        for idx, similarity in compared_documents.items():
            print(f"Document: {idx}, similarity: {similarity:.2f}%")
            
            
    def title(self, document):
        results = []
        #Binarized and Unigram
        document_matrix = binary_title.unigramVocabulary.transform(document).toarray()
        matrix = binary_title.unigram_matrix()
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "Binarized", "Unigram", "Title",  similarity])
            
        #Binarized and Bigram
        document_matrix = binary_title.bigramVocabulary.transform(document).toarray()
        matrix = binary_title.bigram_matrix()
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "Binarized", "Bigram", "Title",  similarity])
        
        #Frequency and Unigram
        document_matrix = frequency_title.unigramVocabulary.transform(document).toarray()
        matrix = frequency_title.unigram_matrix()
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "Frequency", "Unigram", "Title",  similarity])
            
        #Frequency and Bigram
        document_matrix = frequency_title.bigramVocabulary.transform(document).toarray()
        matrix = frequency_title.bigram_matrix()
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "Frequency", "Bigram", "Title",  similarity])
        
        #TFIDF Unigram
        document_matrix = tfidf_title.unigramVocabulary.transform(document).toarray()
        matrix = tfidf_title.unigram_matrix()
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "TF-IDF", "Unigram", "Title",  similarity])
        
        #TFIDF Bigram
        document_matrix = tfidf_title.bigramVocabulary.transform(document).toarray()
        matrix = tfidf_title.bigram_matrix()
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "TF-IDF", "Unigram", "Title",  similarity])
        
        return sorted(results, key=lambda x: x[4], reverse=True)[:10]


    def content(self, document):
        results = []
        #Binarized and Unigram
        document_matrix = binary_content.unigramVocabulary.transform(document).toarray()
        matrix = binary_content.unigram_matrix()       
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "Binarized", "Unigram", "Content",  similarity])
            
        #Binarized and Bigram
        document_matrix = binary_content.bigramVocabulary.transform(document).toarray()
        matrix = binary_content.bigram_matrix()
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "Binarized", "Bigram", "Content",  similarity])  
                  
        #Frequency and Unigram
        document_matrix = frequency_content.unigramVocabulary.transform(document).toarray()
        matrix = frequency_content.unigram_matrix()
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "Frequency", "Unigram", "Content",  similarity])
            
        #Frequency and Bigram
        document_matrix = frequency_content.bigramVocabulary.transform(document).toarray()
        matrix = frequency_content.bigram_matrix()        
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "Frequency", "Bigram", "Content",  similarity])
        
        #TFIDF Unigram
        document_matrix = tfidf_content.unigramVocabulary.transform(document).toarray()
        matrix = tfidf_content.unigram_matrix()
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "TF-IDF", "Unigram", "Content",  similarity])
        
        #TFIDF Bigram
        document_matrix = tfidf_content.bigramVocabulary.transform(document).toarray()
        matrix = tfidf_content.bigram_matrix()
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "TF-IDF", "Bigram", "Content",  similarity])
        
        return sorted(results, key=lambda x: x[4], reverse=True)[:10]

    def title_content(self, document):
        results = []
        #Binarized and Unigram
        document_matrix = binary_title_content.unigramVocabulary.transform(document).toarray()
        matrix = binary_title_content.unigram_matrix()
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "Binarized", "Unigram", "Title + Content",  similarity])
            
        #Binarized and Bigram
        document_matrix = binary_title_content.bigramVocabulary.transform(document).toarray()
        matrix = binary_title_content.bigram_matrix()      
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "Binarized", "Bigram", "Title + Content",  similarity])
        
        #Frequency and Unigram
        document_matrix = frequency_title_content.unigramVocabulary.transform(document).toarray()
        matrix = frequency_title_content.unigram_matrix()
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "Frequency", "Unigram", "Title + Content",  similarity])
            
        #Frequency and Bigram
        document_matrix = frequency_title_content.bigramVocabulary.transform(document).toarray()
        matrix = frequency_title_content.bigram_matrix()
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "Frequency", "Bigram", "Title + Content",  similarity])
        
        #TFIDF Unigram
        document_matrix = tfidf_title_content.unigramVocabulary.transform(document).toarray()
        matrix = tfidf_title_content.unigram_matrix()
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "TF-IDF", "Unigram", "Title + Content",  similarity])
        
        #TFIDF Bigram
        document_matrix = tfidf_title_content.bigramVocabulary.transform(document).toarray()
        matrix = tfidf_title_content.bigram_matrix()
        
        for idx in range(n):
            similarity = self.cosine(document_matrix[0], matrix[idx])
            results.append([idx, "TF-IDF", "Bigram", "Title + Content",  similarity])
        
        return sorted(results, key=lambda x: x[4], reverse=True)[:10]

    def generar_pdf(self, data):
        doc = SimpleDocTemplate("Individual Performance.pdf", pagesize=letter)
        tabla = Table(data)
        estilo = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.saddlebrown),
                             ('SPAN', (0, 0), (-1, 0)),  
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, 1), colors.lightblue),
                            ('BACKGROUND', (0, 2), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        tabla.setStyle(estilo)
        elementos = [tabla]
        doc.build(elementos)

    def global_test(self, document):
        global_results = self.title(document)
        global_results += self.content(document)
        global_results += self.title_content(document)
        
        global_results = sorted(global_results, key=lambda x: x[4], reverse=True)[:10]
        global_results.insert(0, ["Corpus Document", "Vector Representation", "Extracted Features", "Comparison Element", "Similarity"])
        
        table_title = self.__text__.split()
        if len(table_title) > 15:
            table_title = table_title[:14]
            self.__text__ = " ".join(table_title)
            self.__text__ += " ..."
        global_results.insert(0, [self.__text__])
        
        self.generar_pdf(global_results)
        return global_results
