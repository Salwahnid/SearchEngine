import React, { useState } from "react";
import { AiOutlineGlobal } from "react-icons/ai"; // Icône de globe
import { FiSun, FiMoon } from "react-icons/fi"; // Icônes clair/sombre

const Navbar = ({ onChangeLanguage }) => {
  const [darkMode, setDarkMode] = useState(false);
  const [showLanguageMenu, setShowLanguageMenu] = useState(false); // État pour afficher/cacher le menu
  const [selectedLanguage, setSelectedLanguage] = useState("fr"); // Langue sélectionnée

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.documentElement.classList.toggle("dark");
  };

  const handleLanguageChange = (lang) => {
    setSelectedLanguage(lang);
    onChangeLanguage(lang); // Passer la langue choisie au parent (App.js)
    setShowLanguageMenu(false); // Fermer le menu après sélection
  };

  return (
    <nav className="flex items-center justify-between px-4 py-2">
      {/* Logo */}
      <div className="flex items-center">
        <img src="/logo.png" alt="Logo" className="h-16 w-32 mr-2" />
      </div>

      {/* Icônes */}
      <div className="flex items-center space-x-4">
        {/* Bouton pour changer de langue */}
        <div className="relative">
          <button
            className="text-gray-600 hover:text-gray-800 dark:text-gray-300 dark:hover:text-gray-100"
            onClick={() => setShowLanguageMenu(!showLanguageMenu)} // Afficher le menu déroulant
          >
            <AiOutlineGlobal className="text-2xl" />
          </button>

          {showLanguageMenu && (
            <div className="absolute right-0 mt-2 w-16 bg-white shadow-lg rounded-lg z-10 dark:text-white dark:bg-gray-700">
              <ul className="flex flex-col p-2">
                <li
                  className="cursor-pointer p-2 hover:bg-gray-100 dark:hover:bg-gray-600"
                  onClick={() => handleLanguageChange("fr")}
                >
                  Fr
                </li>
                <li
                  className="cursor-pointer p-2 hover:bg-gray-100 dark:hover:bg-gray-600"
                  onClick={() => handleLanguageChange("ar")}
                >
                  Ar
                </li>
                <li
                  className="cursor-pointer p-2 hover:bg-gray-100 dark:hover:bg-gray-600"
                  onClick={() => handleLanguageChange("en")}
                >
                  En
                </li>
              </ul>
            </div>
          )}
        </div>

        {/* Bouton pour mode clair/sombre */}
        <button
          className="text-gray-600 hover:text-gray-800 dark:text-gray-300 dark:hover:text-gray-100"
          onClick={toggleDarkMode}
        >
          {darkMode ? (
            <FiSun className="text-2xl" />
          ) : (
            <FiMoon className="text-2xl" />
          )}
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
