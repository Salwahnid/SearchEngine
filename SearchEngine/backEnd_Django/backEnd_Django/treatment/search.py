from indexation import preprocess_text, store_query_index
from collections import defaultdict
import sqlite3
from math import log

# Fonction pour calculer le TF-IDF
def compute_tfidf(db_connection, query_tokens):
    cursor = db_connection.cursor()
    
    # 1. Récupérer tous les documents
    cursor.execute('SELECT DISTINCT doc_id FROM inverted_index')
    all_docs = cursor.fetchall()
    total_docs = len(all_docs)

    # 2. Calculer l'IDF pour chaque terme
    idf_scores = {}
    for term in query_tokens:
        cursor.execute('SELECT DISTINCT doc_id FROM inverted_index WHERE term=?', (term,))
        doc_freq = len(cursor.fetchall())
        if doc_freq > 0:
            idf_scores[term] = log(total_docs / doc_freq)

    return idf_scores

# Fonction pour rechercher les documents qui contiennent les termes de la requête
def search_documents(query, db_connection):
    # 1. Indexation de la requête dans la table `query_index` avant la recherche
    store_query_index(query, db_connection)

    # Tokenisation et traitement de la requête
    query_tokens = preprocess_text(query)
    cursor = db_connection.cursor()

    # 2. Récupérer les termes de la requête et leurs fréquences depuis la table `query_index`
    query_terms = {}
    for pos, token in enumerate(query_tokens):
        cursor.execute('SELECT frequency FROM query_index WHERE term=? AND query_id=?', (token, 1))
        freq = cursor.fetchone()
        if freq:
            query_terms[token] = freq[0]

    # 3. Calculer l'IDF des termes dans la requête
    idf_scores = compute_tfidf(db_connection, query_tokens)

    # 4. Calculer la similarité entre la requête et chaque document, et récupérer les positions et fréquences
    doc_scores = defaultdict(float)  # Utilisation de float pour le calcul des scores
    doc_positions = defaultdict(list)  # Dictionnaire pour stocker les positions et fréquences des termes dans chaque document

    # Pour chaque terme dans la requête, chercher les documents correspondants dans `inverted_index`
    for term, query_freq in query_terms.items():
        cursor.execute('SELECT doc_id, position, frequency FROM inverted_index WHERE term=?', (term,))
        rows = cursor.fetchall()
        term_idf = idf_scores.get(term, 0)  # IDF pour le terme
        for doc_id, position, doc_freq in rows:
            # Calculer le score TF-IDF pour chaque document basé sur la fréquence du terme dans le document et la requête
            tfidf_score = query_freq * term_idf * doc_freq
            doc_scores[doc_id] += tfidf_score  # Ajouter au score du document
            doc_positions[doc_id].append((term, position, doc_freq))  # Stocker le terme, sa position et sa fréquence

    # 5. Trier les documents par score TF-IDF décroissant
    ranked_documents = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

    # 6. Préparer les résultats avec les positions et fréquences des termes dans les documents
    results = []
    for doc_id, score in ranked_documents:
        positions_and_freqs = doc_positions[doc_id]
        results.append((doc_id, score, positions_and_freqs))

    return results

if __name__ == "__main__":
    db_file = "inverted_index.db"  # Nom de la base de données SQLite

    # Connexion à la base de données SQLite
    db_connection = sqlite3.connect(db_file)

    # Recherche des documents pertinents pour la requête
    query = "analyse analyse données analyse des données pour la recherche"
    print(f"Recherche des documents pour la requête : '{query}'")

    # Recherche des documents pertinents pour la requête
    ranked_docs = search_documents(query, db_connection)
    print("\nDocuments correspondants à la requête :")
    for doc_id, score, positions_and_freqs in ranked_docs:
        print(f"Document ID: {doc_id}, Score (TF-IDF): {score}")  # Display the TF-IDF score
        print("Positions et fréquences des termes :")
        for term, position, freq in positions_and_freqs:
            print(f"Terme: '{term}', Position: {position}, Fréquence dans le document: {freq}")

    # Fermeture de la connexion à la base de données
    db_connection.close()