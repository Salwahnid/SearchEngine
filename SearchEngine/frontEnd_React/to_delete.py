from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sqlite3
from .treatment.Indexation import preprocess_text  # Utiliser la fonction preprocess_text de votre script d'indexation
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Fonction pour charger les documents depuis la base de données
def load_documents_from_db(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SELECT DISTINCT doc_id, GROUP_CONCAT(term, " ") as content FROM inverted_index GROUP BY doc_id')
    rows = cursor.fetchall()
    doc_ids = [row[0] for row in rows]
    documents = [row[1] for row in rows]
    print("Documents loaded from DB:", documents)  # Ligne de débogage
    return doc_ids, documents

# Fonction de recherche vectorielle
def vectorial_search(query, documents, doc_ids):
    vectorizer = TfidfVectorizer()

    # Combine documents and query
    all_texts = documents + [query]  
    
    # Assurez-vous que tout est sous forme de chaîne
    all_texts = [str(text) if isinstance(text, str) else ' '.join(text) for text in all_texts]
    
    # Transformez les textes en matrices TF-IDF
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Le dernier vecteur correspond au vecteur de la requête
    query_vector = tfidf_matrix[-1]
    doc_vectors = tfidf_matrix[:-1]
    
    # Calcul de la similarité cosinus
    similarities = cosine_similarity(query_vector, doc_vectors).flatten()
    
    # Tri des documents par pertinence
    ranked_indices = np.argsort(similarities)[::-1]
    
    # Limiter aux 5 premiers résultats
    ranked_results = [(doc_ids[idx], similarities[idx]) for idx in ranked_indices[:5]]
    
    return ranked_results

# Vue API pour la recherche
class SearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', None)  # Récupère la requête de recherche depuis les paramètres GET
        
        if not query:
            return Response({"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Connexion à la base de données SQLite
        db_file = "inverted_index.db"
        db_connection = sqlite3.connect(db_file)

        try:
            # Charger les documents depuis la base de données
            doc_ids, documents = load_documents_from_db(db_connection)

            # Prétraiter les documents
            documents = [preprocess_text(doc) for doc in documents]

            # Prétraiter la requête
            query = preprocess_text(query)

            # Effectuer la recherche par similarité vectorielle
            results = vectorial_search(query, documents, doc_ids)

            # Retourner les résultats sous forme de JSON
            result_list = [{'doc_id': doc_id, 'score': round(score, 2)} for doc_id, score in results]
            return Response(result_list)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        finally:
            db_connection.close()
