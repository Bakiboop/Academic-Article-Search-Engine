# Import necessary libraries and functions
from math import log
from collections import Counter


def BM25_SEARCH(inverted_index_titles, inverted_index_authors, inverted_index_abstracts, cleaned_titles, cleaned_authors, cleaned_abstracts, query_terms, top_n=10, k1=1.5, b=0.75):
    # Calculate the average document length
    avg_doc_length_titles = sum(len(doc) for doc in cleaned_titles) / len(cleaned_titles)
    avg_doc_length_authors = sum(len(doc) for doc in cleaned_authors) / len(cleaned_authors)
    avg_doc_length_abstracts = sum(len(doc) for doc in cleaned_abstracts) / len(cleaned_abstracts)

    # Dictionary to store scores
    doc_scores = {}

    # Loop through all documents (titles, authors, abstracts)
    for doc_index in range(len(cleaned_titles)):

        # Calculate the length of each document
        doc_length_titles = len(cleaned_titles[doc_index])
        doc_length_authors = len(cleaned_authors[doc_index])
        doc_length_abstracts = len(cleaned_abstracts[doc_index])
        score = 0

        # Loop through each query term
        for term in query_terms:
            # Calculate Term Frequency (TF)
            term_freq_titles = cleaned_titles[doc_index].count(term)
            term_freq_authors = cleaned_authors[doc_index].count(term)
            term_freq_abstracts = cleaned_abstracts[doc_index].count(term)

            # Calculate Document Frequency (DF) for Inverse Document Frequency (IDF)
            doc_freq_titles = len(inverted_index_titles.get(term, []))
            doc_freq_authors = len(inverted_index_authors.get(term, []))
            doc_freq_abstracts = len(inverted_index_abstracts.get(term, []))

            # Calculate IDF
            idf_titles = log((len(cleaned_titles) - doc_freq_titles + 0.5) / (doc_freq_titles + 0.5) + 1.0)
            idf_authors = log((len(cleaned_authors) - doc_freq_authors + 0.5) / (doc_freq_authors + 0.5) + 1.0)
            idf_abstracts = log((len(cleaned_abstracts) - doc_freq_abstracts + 0.5) / (doc_freq_abstracts + 0.5) + 1.0)

            # Calculate Okapi BM25 score for each section
            term_score_titles = idf_titles * (term_freq_titles * (k1 + 1)) / (term_freq_titles + k1 * (1 - b + b * doc_length_titles / avg_doc_length_titles))
            term_score_authors = idf_authors * (term_freq_authors * (k1 + 1)) / (term_freq_authors + k1 * (1 - b + b * doc_length_authors / avg_doc_length_authors))
            term_score_abstracts = idf_abstracts * (term_freq_abstracts * (k1 + 1)) / (term_freq_abstracts + k1 * (1 - b + b * doc_length_abstracts / avg_doc_length_abstracts))

            # Add the scores (may need adjustment based on context)
            score += term_score_titles + term_score_authors + term_score_abstracts

        # Store the score for the current document
        doc_scores[doc_index] = score

    # Sort documents based on their scores in descending order
    top_indices = sorted(doc_scores, key=doc_scores.get, reverse=True)[:top_n]

    return top_indices
