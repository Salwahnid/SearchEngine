import sqlite3
from Indexation import preprocess_text  # Use the preprocess_text function from your indexation script
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to load indexed documents from the database
def load_documents_from_db(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SELECT DISTINCT doc_id, GROUP_CONCAT(term, " ") as content FROM inverted_index GROUP BY doc_id')
    rows = cursor.fetchall()
    doc_ids = [row[0] for row in rows]
    documents = [row[1] for row in rows]
    print("Documents loaded from DB:", documents)  # Debugging line
    return doc_ids, documents

# Function to calculate vector similarity
def vectorial_search(query, documents, doc_ids):
    vectorizer = TfidfVectorizer()
    
    # Combine documents and query
    all_texts = documents + [query]  
    
    # Debugging: Check the contents of all_texts
    print("Contents of all_texts:", all_texts)
    print("Types of elements in all_texts:", [type(text) for text in all_texts])
    
    # Ensure all elements are strings
    all_texts = [str(text) if isinstance(text, str) else ' '.join(text) for text in all_texts]
    
    # Now you can safely call fit_transform
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # The last line corresponds to the query vector
    query_vector = tfidf_matrix[-1]
    doc_vectors = tfidf_matrix[:-1]
    
    # Calculate cosine similarity
    similarities = cosine_similarity(query_vector, doc_vectors).flatten()
    
    # Sort documents by relevance
    ranked_indices = np.argsort(similarities)[::-1]
    ranked_results = [(doc_ids[idx], similarities[idx]) for idx in ranked_indices]
    return ranked_results

if __name__ == "__main__":
    db_file = "inverted_index.db"
    db_connection = sqlite3.connect(db_file)

    # Load documents from the database
    doc_ids, documents = load_documents_from_db(db_connection)

    # Preprocess documents using the function from the indexing file
    documents = [preprocess_text(doc) for doc in documents]

    # Ensure all documents are strings
    documents = [str(doc) for doc in documents]

    # User query
    query = "article"
    query = preprocess_text(query)  # Preprocess the query as well

    # Debugging: Check data types
    print("Checking data types...")
    #print([type(doc) for doc in documents])  # Ensure all are strings
    #print(type(query))  # Check that the query is a string

    # Perform vector similarity search
    results = vectorial_search(query, documents, doc_ids)

    # Display results
    print("\nSearch results sorted by relevance:")
    for doc_id, score in results:
        print(f"Document ID: {doc_id} | Similarity: {score:.2f}")

    # Close the database connection
    db_connection.close()