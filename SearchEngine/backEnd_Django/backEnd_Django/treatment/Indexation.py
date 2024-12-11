import os
import nltk
import sqlite3
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from PyPDF2 import PdfReader


# Téléchargement des ressources nécessaires
nltk.download('stopwords')
nltk.download('punkt_tab')

# Définition des stopwords et du stemmer pour le français
stop_words = set(stopwords.words('french'))
stemmer = SnowballStemmer('french')

# Fonction de prétraitement
def preprocess_text(text):
    tokens = nltk.word_tokenize(text.lower())  # Tokenisation et conversion en minuscules
    filtered_tokens = [stemmer.stem(word) for word in tokens if word.isalnum() and word not in stop_words]
    return filtered_tokens

# Fonction pour lire le contenu d'un fichier PDF
def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()  # Extraction du texte de chaque page
    return text

# Fonction pour construire l'index inversé avec fréquences et positions
def build_and_store_inverted_index(directory, db_connection):
    cursor = db_connection.cursor()
    
    # Création ou modification de la table pour inclure la position et la fréquence
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inverted_index (
            term TEXT,
            doc_id INTEGER,
            position INTEGER,
            frequency INTEGER,
            PRIMARY KEY (term, doc_id, position)
        )
    ''')
    print("Table 'inverted_index' créée ou déjà existante.")

    # Parcours des fichiers dans le dossier
    for doc_id, filename in enumerate(os.listdir(directory)):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            print(f"Traitement du fichier : {filename}")
            content = read_pdf(file_path)
            tokens = preprocess_text(content)

            # Insertion des termes avec leurs positions et fréquences
            for pos, token in enumerate(tokens):
                cursor.execute('''
                    INSERT OR IGNORE INTO inverted_index (term, doc_id, position, frequency)
                    VALUES (?, ?, ?, ?)
                ''', (token, doc_id, pos, tokens.count(token)))
    
    db_connection.commit()

# Fonction pour indexer une requête avec fréquences et positions correctes
def store_query_index(query, db_connection):
    tokens = preprocess_text(query)
    cursor = db_connection.cursor()

    # Identifier un ID unique pour la requête
    query_id = 1

    # Créer ou modifier la table pour inclure la position et la fréquence
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS query_index (
            term TEXT,
            query_id INTEGER,
            position INTEGER,
            frequency INTEGER,
            PRIMARY KEY (term, query_id, position)
        )
    ''')

    # Insertion des termes avec leurs positions et fréquences
    for pos, token in enumerate(tokens):
        cursor.execute('''
            INSERT OR IGNORE INTO query_index (term, query_id, position, frequency)
            VALUES (?, ?, ?, ?)
        ''', (token, query_id, pos, tokens.count(token)))
    
    db_connection.commit()
    print(f"Indexation de la requête terminée. ID de la requête : {query_id}")

# Fonction pour afficher l'index inversé à partir de la base de données
def display_inverted_index(db_connection, table_name):
    cursor = db_connection.cursor()
    cursor.execute(f'''
        SELECT term, doc_id, position, frequency FROM {table_name}
        ORDER BY term, doc_id, position
    ''')
    
    rows = cursor.fetchall()
    for row in rows:
        print(f"Mot : '{row[0]}' | Document/Requête : {row[1]} | Position : {row[2]} | Fréquence : {row[3]}")

if __name__ == "__main__":
    pdf_directory = "backEnd_Django/data/code_penal_split_files"  # Chemin du dossier des PDF
    db_file = "inverted_index.db"  # Nom de la base de données SQLite

    # Connexion à la base de données SQLite
    db_connection = sqlite3.connect(db_file)

    # Indexation des documents
    if os.path.isdir(pdf_directory):
        build_and_store_inverted_index(pdf_directory, db_connection)
    else:
        print(f"Le dossier spécifié n'existe pas : {pdf_directory}")

    # Indexation d'une requête
    query = "Sanctions pour fraude fiscale"
    print(f"Indexation de la requête : '{query}'")
    store_query_index(query, db_connection)

    # Afficher l'index inversé des documents
    print("\nIndex inversé des documents :")
    display_inverted_index(db_connection, "inverted_index")

    # Afficher l'index des requêtes
    print("\nIndex des requêtes :")
    cursor = db_connection.cursor()
    cursor.execute('SELECT term, query_id, position, frequency FROM query_index ORDER BY term, query_id, position')
    rows = cursor.fetchall()
    for row in rows:
        print(f"Mot : '{row[0]}' | Requête : {row[1]} | Position : {row[2]} | Fréquence : {row[3]}")

    # Fermeture de la connexion à la base de données
    db_connection.close()
