# -*- coding: utf-8 -*-

def Boolean_Search(index_abs, index_titles, index_authors, query):
    p0 = 0
    operators = ['and', 'or', 'not']

    # Search for the first query term in abstracts, titles, and authors
    key = query[p0]
    abstract = list(index_abs.get(key, []))
    titles = list(index_titles.get(key, []))
    authors = list(index_authors.get(key, []))

    # Combine all results, keep only unique document IDs, and sort them
    result = abstract + titles + authors
    unique_keys = list(set(result))
    result = sorted(unique_keys)

    # Move to the next token, which should be an operator
    p0 += 1

    while p0 < len(query):
        # If the token is an operator
        if query[p0] in operators:
            p0 += 1

        # Look for the next term after the operator
        key = query[p0]

        # Search for the term in abstracts, titles, and authors
        abstract = list(index_abs.get(key, []))
        titles = list(index_titles.get(key, []))
        authors = list(index_authors.get(key, []))

        # Combine and sort the postings
        posting = abstract + titles + authors
        unique_keys = list(set(posting))
        posting = sorted(unique_keys)

        # Depending on the operator, call the corresponding function
        if query[p0 - 1] == 'and':
            result = and_postings(result, posting)
        elif query[p0 - 1] == 'not':
            result = not_postings(posting, result)
        else:
            result = or_postings(result, posting)
        p0 += 1

    return result

# Functions for Boolean Search

# OR Operator
def or_postings(posting1, posting2):

    # Pointers for the lists
    p1 = 0
    p2 = 0

    # Final result list
    result = list()

    # Iterate until one list is exhausted
    while p1 < len(posting1) and p2 < len(posting2):
        if posting1[p1] == posting2[p2]:  # If both have the same document ID
            result.append(posting1[p1])  # Store one of them
            # Move to the next in both lists
            p1 += 1
            p2 += 1

        # Check which document ID is smaller to append first
        elif posting1[p1] > posting2[p2]:
            result.append(posting2[p2])
            p2 += 1
        else:
            result.append(posting1[p1])
            p1 += 1

    # If one list is not fully traversed, append the remaining elements
    while p1 < len(posting1):
        result.append(posting1[p1])
        p1 += 1

    while p2 < len(posting2):
        result.append(posting2[p2])
        p2 += 1

    return result

# AND Operator
def and_postings(posting1, posting2):
    p1 = 0
    p2 = 0
    result = list()
    while p1 < len(posting1) and p2 < len(posting2):
        if posting1[p1] == posting2[p2]:
            result.append(posting1[p1])
            p1 += 1
            p2 += 1

        elif posting1[p1] > posting2[p2]:
            p2 += 1
        else:
            p1 += 1

    return result

# NOT Operator
def not_postings(posting, indexed_docIDs):
    # Complement of an empty list is the list of all indexed document IDs
    if not posting:
        return indexed_docIDs
    else:
        p1 = 0
        p2 = 0

        while p1 < len(posting) and p2 < len(indexed_docIDs):
            if posting[p1] == indexed_docIDs[p2]:
                indexed_docIDs.remove(posting[p1])  # Remove matching element from the list
                p1 += 1
                p2 += 1

            elif posting[p1] > indexed_docIDs[p2]:
                p2 += 1
            else:
                p1 += 1

    return indexed_docIDs
