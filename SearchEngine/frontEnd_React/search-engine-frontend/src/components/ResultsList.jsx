import React from 'react';

const ResultsList = ({ results, noResultsText }) => {
  console.log("Results:", results);
  return (
    <div className="mt-8">
      {results.length === 0 ? (
        <p className="text-center">{noResultsText}</p>
      ) : (
        <ul>
          {results.map((result, index) => {
            const fileUrl = result.file_url ? `http://localhost:8000/${result.file_url}` : null;
            return (
              <li key={result.file_name} className="mb-4">
                <div className="bg-gray-100 p-4 rounded">
                  {/* Affichage du nom du fichier et lien pour l'ouvrir */}
                  <h3 className="text-xl font-semibold">
                    <a
                      href={fileUrl} // Utilisation de fileUrl construit pour chaque fichier
                      target="_blank" // Ouvrir dans un nouvel onglet
                      rel="noopener noreferrer" // Sécurité pour éviter les attaques XSS
                      className="text-blue-600 hover:underline"
                    >
                      {result.file_name} {/* Nom du fichier */}
                    </a>
                  </h3>
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
};

export default ResultsList;
