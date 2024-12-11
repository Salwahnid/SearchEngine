import os
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sqlite3
from .treatment.Indexation import preprocess_text  # Utiliser la fonction preprocess_text de votre script d'indexation
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import traceback  # Pour obtenir la trace complète des erreurs

file_paths= None
# Fonction pour charger les documents depuis la base de données
def load_documents_from_db(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SELECT * FROM documents')
    rows = cursor.fetchall()
    print(f"Rows fetched from DB: {rows}")
    doc_ids = [row[0] for row in rows]
    documents = [row[3] for row in rows]
    file_names = [row[2] for row in rows]
    file_paths = [row[1] for row in rows]

    return doc_ids, documents, file_names, file_paths

def preprocess_text(text):
    if not text:
        return ""  # Retourner une chaîne vide si le texte est vide
    return " ".join(text.lower().split())  # Simple prétraitement

def vectorial_search(query, documents, doc_ids):
    if not query or not documents or not doc_ids:
        raise ValueError("La requête, les documents ou les identifiants de documents sont vides.")
    
    vectorizer = TfidfVectorizer()
    
    # Prétraitement des documents
    all_texts = [doc for doc in documents if doc.strip()]  # Enlever les documents vides
    if not all_texts:
        raise ValueError("Tous les documents sont vides après prétraitement.")
    
    all_texts.append(query)  # Ajouter la requête
    
    # Transformation en matrices TF-IDF
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    #print(f"TF-IDF Matrix shape: {tfidf_matrix.shape}")
    
    query_vector = tfidf_matrix[-1]
    doc_vectors = tfidf_matrix[:-1]
    
    if np.all(query_vector.toarray() == 0):
        raise ValueError("Le vecteur de la requête est nul (tous les mots sont absents).")
    if np.all(doc_vectors.toarray() == 0):
        raise ValueError("Tous les documents ont des vecteurs nuls.")
    
    similarities = cosine_similarity(query_vector, doc_vectors).flatten()

    ranked_indices = np.argsort(similarities)[::-1]

    ranked_results = [(doc_ids[idx], similarities[idx]) for idx in ranked_indices[:5]]

    # Afficher les similitudes dans la console
    print("Cosine similarities for the top 5 documents:")
    for idx, (doc_id, similarity) in enumerate(ranked_results):
        print(f"Doc ID: {doc_id}, Similarity: {similarity:.4f}")

    return ranked_results


def get_file_url(file_paths, idx):
    # Récupérer le chemin absolu du fichier à l'index donné
    file_path = file_paths[idx]
    
    # Rendre le chemin relatif en supprimant la partie du chemin qui correspond à MEDIA_ROOT
    relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
    
    # Générer l'URL du fichier en combinant MEDIA_URL et le chemin relatif
    file_url = settings.MEDIA_URL + relative_path
    
    return file_url

# Vue API pour la recherche
class SearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', None)
        
        if not query:
            return Response({"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)

        db_file = r".\inverted_index.db"
        #db_file = r"C:\Users\pc\Documents\Projects\SearchEngine\SearchEngine\inverted_index.db"

        db_connection = sqlite3.connect(db_file)

        try:
            # Charger les documents depuis la base de données
            doc_ids, documents, file_names, file_paths = load_documents_from_db(db_connection)
            print(f"Loaded {len(doc_ids)} documents.")  # Vérification du nombre de documents
            print(f"id {doc_ids} documents.")  # Vérification du nombre de documents

            if not doc_ids:  # Si aucun document n'est trouvé dans la base de données
                return Response({"error": "No documents found in the database."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Traiter les documents
            print("Preprocessing documents...")  # Message de log pour le prétraitement
            documents = [preprocess_text(doc) for doc in documents]
            query = preprocess_text(query)

            # Rechercher les résultats
            print(f"Query after preprocessing: {query[:100]}...")  # Affiche le début de la requête après prétraitement
            results = vectorial_search(query, documents, doc_ids)
            print(f"Search results: {results}")  # Log des résultats de la recherche

            if not results:  # Si aucun résultat n'est trouvé
                return Response({"error": "No matching documents found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Construire la liste des résultats
            result_list = []
            for idx, (doc_id, score) in enumerate(results):
                doc_index = doc_ids.index(doc_id)  # Trouver l'index réel du document dans la liste doc_ids
                file_name = file_names[doc_index]  # Récupérer le nom du fichier
                file_url = get_file_url(file_paths, doc_index)  # Construire l'URL du fichier PDF à partir du bon index
    
                result_list.append({
                    'file_name': file_name,
                    'file_url': file_url,
                    'score': round(score, 2)
                })


            print(f"Search results: {result_list}") 
            return Response(result_list)

        except Exception as e:
            # Log de l'erreur complète
            return Response({"error": f"An error occurred: {str(e)}", "trace": traceback.format_exc()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        finally:
            if db_connection:
                db_connection.close()