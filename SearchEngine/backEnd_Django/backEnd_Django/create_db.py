import os
import sqlite3
import pdfplumber  # Pour extraire le texte des fichiers PDF

# Connexion à la base de données SQLite
db_file = 'inverted_index.db'
connection = sqlite3.connect(db_file)
cursor = connection.cursor()

# Créer la table documents (si elle n'existe pas déjà) avec un champ pour le titre
cursor.execute('''
CREATE TABLE IF NOT EXISTS documents (
    doc_id INTEGER PRIMARY KEY,
    file_path TEXT NOT NULL,
    title TEXT,  -- Ajouter un champ pour le titre
    content TEXT
);
''')

# Fonction pour extraire le texte d'un fichier PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Fonction pour extraire le titre du fichier PDF (par exemple, la première ligne)
def extract_title_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]  # Prendre la première page pour extraire le titre
        text = first_page.extract_text()
        # Retourner la première ligne comme titre (ou une autre logique selon besoin)
        title = text.split('\n')[0] if text else "Untitled"
    return title

# Fonction pour insérer un document dans la base de données
def insert_document(doc_id, file_path, title, content):
    cursor.execute('''
    INSERT INTO documents (doc_id, file_path, title, content)
    VALUES (?, ?, ?, ?)
    ''', (doc_id, file_path, title, content))
    connection.commit()

# Fonction pour parcourir un répertoire et ajouter tous les fichiers PDF
def insert_documents_from_directory(directory):
    doc_id = 1  # Commencer avec un doc_id arbitraire
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):  # Si c'est un fichier PDF
            file_path = os.path.join(directory, filename)
            content = extract_text_from_pdf(file_path)  # Extraire le texte du fichier PDF
            title = extract_title_from_pdf(file_path)  # Extraire le titre du fichier PDF
            insert_document(doc_id, file_path, title, content)  # Insérer dans la base de données
            doc_id += 1  # Incrémenter le doc_id pour chaque fichier

# Exemple d'utilisation
directory = 'C:\\Users\\pc\\Documents\\Projects\\SearchEngine\\SearchEngine\\SearchEngine\\backEnd_Django\\backEnd_Django\\data\\code_penal_split_files'
insert_documents_from_directory(directory)

# Fermer la connexion à la base de données
connection.close()

print("Documents PDF ajoutés à la base de données avec succès!")
