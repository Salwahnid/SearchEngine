import sqlite3

# Fonction pour vérifier si une table existe
def check_if_table_exists(db_connection, table_name):
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cursor.fetchone()
    return result is not None

# Exemple d'utilisation
db_file = r"C:\Users\pc\Documents\Projects\SearchEngine\SearchEngine\inverted_index.db"  # Utilisation d'un chemin brut (r"")

# Connexion à la base de données
db_connection = sqlite3.connect(db_file)

# Vérifier si la table 'documents' existe
if check_if_table_exists(db_connection, 'documents'):
    print("La table 'documents' existe.")
    
    # Exécuter une requête pour récupérer des données
    cursor = db_connection.cursor()
    cursor.execute('SELECT * FROM documents')
    
    # Récupérer les résultats (optionnel)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
else:
    print("La table 'documents' n'existe pas.")

# Fermer la connexion après utilisation
db_connection.close()
