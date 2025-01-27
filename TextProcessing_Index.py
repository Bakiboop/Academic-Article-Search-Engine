import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Split data into categories
def split_categories(data, type_data):
    all_type_data = []
    for entry in data:
        entries = entry[type_data]
        all_type_data.append(entries.lower())  # Convert to lowercase (authors won't undergo text processing)
    return all_type_data

# Text processing function
def process_paper(paper, type_paper):
    # Abstracts and titles go through all processing steps
    # Queries skip stop word removal
    # Authors are only tokenized to preserve full names

    if type_paper == 'authors' or type_paper == 'dates':
        tokens = []
        for author in paper.split(', '):
            tokens.append(author)
        stemmed_paper = tokens
    else:
        # Tokenization
        tokens = word_tokenize(paper)

        # Stemming
        porter = PorterStemmer()
        stemmed_paper = [porter.stem(t) for t in tokens]

        if type_paper != 'query':
            # Remove stop words and punctuation
            stopwords = nltk.corpus.stopwords.words('english')
            cleaned_tokens = []

            for token in stemmed_paper:
                if token not in string.punctuation and token not in stopwords:
                    cleaned_tokens.append(token)

            return cleaned_tokens
    return stemmed_paper

# Create inverted index
def invert_index(data):
    # Create a dictionary that tracks where terms appear
    inverted_list = {}

    for data_id, doc_list in enumerate(data):  # Enumerate pairs index and content
        for doc in doc_list:
            # Split each term individually
            if doc in inverted_list:  # If the term exists, add the index where it was found
                inverted_list[doc].add(data_id)
            else:
                inverted_list[doc] = {data_id}  # Otherwise, add the term with the index

    # Sort the terms in the inverted index
    sorted_inverted_list = {}
    for term, doc_ids in inverted_list.items():
        sorted_doc_ids = sorted(doc_ids)
        sorted_inverted_list[term] = sorted_doc_ids

    return sorted_inverted_list  # Return the sorted inverted list
