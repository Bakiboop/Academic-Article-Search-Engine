# -*- coding: utf-8 -*-
import json
import sys
from Boolean_Search import *
from TextProcessing_Index import *
from nltk.tokenize import word_tokenize
from VSM_SEARCH import *
from BM25_SEARCH import *

# Main function to handle search queries, types, and filters
def main(search_query, search_type, filter_type, filter_search):
    # Open the JSON file containing the data
    with open('arx.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Store all titles
    all_titles = split_categories(data, 'title')

    # Store all abstracts
    all_abs = split_categories(data, 'abstract')

    # Store authors separately
    all_authors = split_categories(data, 'authors')

    # Store all dates
    all_dates = split_categories(data, 'date')

    # Text processing

    # Process abstracts
    cleaned_abs = [process_paper(abstract, 'abs') for abstract in all_abs]

    # Process titles
    cleaned_titles = [process_paper(title, 'titles') for title in all_titles]

    # Process authors (split into individual names)
    cleaned_authors = [process_paper(author, 'authors') for author in all_authors]

    # Process dates
    cleaned_dates = [process_paper(date.rstrip(' ('), 'dates') for date in all_dates]

    # Process user query (do not remove stop words to preserve operators like AND, OR, NOT)
    cleaned_search_query = process_paper(search_query, 'query')

    # Create inverted indices
    invert_index_abs = invert_index(cleaned_abs)  # Inverted index for abstracts
    invert_index_titles = invert_index(cleaned_titles)  # Inverted index for titles
    invert_index_authors = invert_index(cleaned_authors)  # Inverted index for authors

    # Perform search based on the specified type
    if search_type == 'boolean':
        result = Boolean_Search(invert_index_abs, invert_index_titles, invert_index_authors, cleaned_search_query)

    elif search_type == 'vsm':
        result = VSM_SEARCH(cleaned_titles, cleaned_abs, cleaned_authors, cleaned_search_query, data)

    elif search_type == 'okapi':
        result = BM25_SEARCH(invert_index_titles, invert_index_authors, invert_index_abs, cleaned_titles, cleaned_authors, cleaned_abs, cleaned_search_query, top_n=30)

    # Apply filters if specified

    # Filter by authors
    if filter_type == 'authors':
        filter_in = list(invert_index_authors.get(filter_search, []))
        # Keep only documents with the specified author
        result = and_postings(result, filter_in)

    # Filter by dates
    elif filter_type == 'date':
        invert_index_dates = invert_index(cleaned_dates)  # Create inverted index for dates
        filter_in = list(invert_index_dates.get(filter_search, []))
        # Keep only documents with the specified date
        result = and_postings(result, filter_in)

    # Collect papers to display
    papers = [data[paper] for paper in result]
    json_file.close()

    print(result)

    return papers

if __name__ == "__main__":
    main()
