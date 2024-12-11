import React, { useState, useEffect } from "react";
import axios from "axios";  // Si tu utilises axios
import SearchBar from './components/SearchBar'; // Assume this is your search bar component
import ResultsList from './components/ResultsList'; // Component for displaying search results
import Navbar from './components/Navbar'; // Assume this is your navbar component

const App = () => {
  const [results, setResults] = useState([]);
  const [language, setLanguage] = useState("fr"); // Langue initiale

  // Fonction pour envoyer la requête de recherche
  const searchHandler = async (query) => {
    try {
      const response = await axios.get("http://localhost:8000/api/search/", {
        params: { query: query, timestamp: new Date().getTime() },  // Ajoute un paramètre unique pour éviter le cache
      });
      console.log("response data",response.data);  
      setResults(response.data);  // Les résultats de l'API Django
    } catch (error) {
      console.error("Erreur lors de la recherche :", error);
    }
  };


  useEffect(() => {
    console.log(results); // Vérifier quand les résultats changent
  }, [results]); 

  // Textes dynamiques pour chaque langue
  const texts = {
    fr: {
      searchPlaceholder: "Rechercher un document...",
      searchButton: "Rechercher",
      noResults: "Aucun résultat trouvé.",
      title: "Moteur de Recherche de Documents",
    },
    ar: {
      searchPlaceholder: "ابحث عن مستند...",
      searchButton: "بحث",
      noResults: "لم يتم العثور على نتائج.",
      title: "محرك بحث المستندات",
    },
    en: {
      searchPlaceholder: "Search for a document...",
      searchButton: "Search",
      noResults: "No results found.",
      title: "Document Search Engine",
    },
  };

  // Fonction pour changer la langue
  const handleChangeLanguage = (lang) => {
    setLanguage(lang); // Changer la langue
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-200 to-white dark:bg-gradient-to-r dark:from-gray-900 dark:to-gray-800 dark:text-white">
      {/* Navbar avec changement de langue */}
      <Navbar onChangeLanguage={handleChangeLanguage} />

      <div className="p-8">
        <h1 className="mb-8 text-3xl font-bold text-center text-blue-600 dark:text-blue-400">
          {texts[language].title}
        </h1>
        {/* Search Bar */}
        <SearchBar
          onSearch={searchHandler}
          placeholder={texts[language].searchPlaceholder}
          buttonText={texts[language].searchButton}
        />
        {/* Liste des résultats */}
        <ResultsList
          results={results}
          noResultsText={texts[language].noResults}
        />
      </div>
    </div>
  );
};

export default App;
