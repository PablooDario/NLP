# Normalized Corpus Package

This package is designed to import vocabularies and transformed documents to document-term matrix from a corpus of news, where there are 3 modules:

- Title
- Content
- Title + content

## Modules

Each module in the package has the following classes:

- binary vectorized
- frequency vectorized
- tf-idf vectorized

## Class

And in turn each **class** has the following attributes and methods:

**Attributes**

- unigram vocabulary $\leadsto$ is the **unigram** vocabulary of the section (Title, Content, Title+Content)
- bigram vocabulary $\leadsto$ is the **bigram** vocabulary of the section

**Methods**

- unigram matrix $\leadsto$ returns the transformed documents to document-term matrix with the unigram vocabulary
- bigram matrix $\leadsto$ returns the transformed documents to document-term matrix with the bigram vocabulary




title, unigram, binary = 0
title, bigram, binary = 0

title, unigram, frequency = 1
title, bigram, frequency = 1

title, unigram, tfidf = 2
title, bigram, tfidf = 2

############################
content, unigram, binary = 3
content, bigram, binary = 3

content, unigram, frequency = 4
content, bigram, frequency = 4

content, unigram, tfidf = 5
content, bigram, tfidf = 5

#########################
title_content, unigram, binary = 6
title_content, bigram, binary = 6

title_content, unigram, frequency = 7
title_content, bigram, frequency = 7

title_content, unigram, tfidf = 8
title_content, bigram, tfidf = 8