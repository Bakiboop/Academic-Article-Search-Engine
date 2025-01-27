from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def VSM_SEARCH(cleaned_titles, cleaned_abs, cleaned_authors, cleaned_search_query, data):
    # Create a combined text that includes title, author, and abstract
    combined_documents = [f"{title} {abstract} {author}" for title, abstract, author in zip(cleaned_titles, cleaned_abs, cleaned_authors)]

    # Use TF-IDF to transform documents into vectors
    vectorizer = TfidfVectorizer()
    # Convert documents into TF-IDF vectors
    docs_vector = vectorizer.fit_transform(combined_documents + [' '.join(cleaned_search_query)])

    # Calculate cosine similarity between documents and the search query
    cosine_similarities = cosine_similarity(docs_vector[:-1], docs_vector[-1])

    # Sort documents based on cosine similarity
    sorted_indices = cosine_similarities.argsort(axis=0)[::-1].flatten()

    # Return the indices of the top 100 most relevant papers
    return sorted_indices[:100]
