import React, { useState } from "react";
import Navbar from "./components/Navbar";
import SearchBar from "./components/SearchBar";
import ResultsList from "./components/ResultsList";

const App = () => {
  const [language, setLanguage] = useState("fr"); // Langue initiale
  const [results, setResults] = useState([]);

  const staticData = [
    { title: "Document 1", snippet: "Ceci est un extrait du document 1." },
    { title: "Document 2", snippet: "Ceci est un extrait du document 2." },
    { title: "Document 3", snippet: "Ceci est un extrait du document 3." },
  ];

  const fetchResults = (query) => {
    const filteredResults = staticData.filter((doc) =>
      doc.title.toLowerCase().includes(query.toLowerCase())
    );
    setResults(filteredResults);
  };

  const handleChangeLanguage = (lang) => {
    setLanguage(lang); // Changer la langue
  };

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

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-200 to-white dark:bg-gradient-to-r dark:from-gray-900 dark:to-gray-800 dark:text-white">
      {/* Navbar avec changement de langue */}
      <Navbar onChangeLanguage={handleChangeLanguage} />

      <div className="p-8">
        <h1 className="mb-8 text-3xl font-bold text-center text-blue-600 dark:text-blue-400">
          {texts[language].title}
        </h1>
        <SearchBar
          onSearch={fetchResults}
          placeholder={texts[language].searchPlaceholder}
          buttonText={texts[language].searchButton}
        />
        <ResultsList
          results={results}
          noResultsText={texts[language].noResults}
        />
      </div>
    </div>
  );
};

export default App;
