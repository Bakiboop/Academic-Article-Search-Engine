# Academic Article Search Engine

This project is a search engine designed for retrieving academic articles efficiently. The system supports multiple search algorithms and provides features like filtering results by authors and dates. Below is a detailed description of its functionality and implementation.

---

## Features

### Search Algorithms
- **Boolean Retrieval**: Allows users to search using operators like AND, OR, NOT. By default, if no operator is specified, the OR operator is used.
- **Vector Space Model (VSM)**: Represents documents and queries as vectors in a multi-dimensional space using TF-IDF, and ranks documents based on cosine similarity.
- **Okapi BM25**: Computes scores using term frequency (TF), inverse document frequency (IDF), and document length, ensuring relevance without bias toward longer documents.

### Filtering Options
- **By Authors**: Filters results to include only articles by specified authors.
- **By Date**: Filters results to include only articles published on specific dates.

---

## Technologies Used

- **Scrapy**: Framework for web crawling, used to collect academic articles from [arXiv](https://arxiv.org).
- **Flask**: Web framework used to build the user interface.
- **scikit-learn**: Used for TF-IDF vectorization and cosine similarity calculations.

---

## Workflow

### 1. Web Crawling
The web crawler collects data from [arXiv](https://arxiv.org) by visiting specific pages containing articles. Extracted fields include:
- **Title**
- **Abstract**
- **Authors**
- **Date of publication**

All collected data is stored in a `papers.json` file for further processing.

### 2. Text Processing
The data undergoes the following preprocessing steps:
- **Normalization**: Converts all text to lowercase.
- **Tokenization**: Splits text into individual words, removing punctuation.
- **Stemming**: Reduces words to their root form.
- **Stop-word Removal**: Removes common words like "and" or "the" (not applied to queries to preserve Boolean operators).

### 3. Inverted Index
An inverted index is built for:
- **Abstracts**
- **Titles**
- **Authors**
- **Dates**

This structure maps each term to the list of documents where it appears, enabling efficient Boolean searches.

### 4. Search Engine
The search engine integrates Boolean Retrieval, VSM, and Okapi BM25, allowing users to search and filter results interactively through a web interface.

---

## How to Use

1. **Run the Application**:
   ```bash
   python flaskblog.py
   ```

2. **Navigate to the Home Page**:
   Access the application at `http://localhost:5000`.

3. **Perform a Search**:
   - Enter a query.
   - Choose a search algorithm (Boolean, VSM, or Okapi BM25).
   - Optionally, apply filters for authors or dates.

4. **View Results**:
   - Results are displayed on the search page.
   - Use filters or perform a new search directly from the results page.

---

## Possible Improvements

- Add support for more complex Boolean queries with parentheses.
- Enhance the user interface for better accessibility and usability.
- Implement spelling correction for user queries.
- Improve crawling rules to avoid duplicate articles.
- Allow real-time crawling for each query instead of relying on pre-crawled data.
- Introduce a ranking mechanism for better relevance in results.


---

## Acknowledgments

This project was developed as part of an academic course on Information Retrieval at the **University of West Attica**, Department of Computer Engineering.

**Contributors**:
- Christos Ioannis Koulmpinta
- Fotis Pallis

Date: 22/01/2024

---

## License

This project is licensed under the MIT License.

