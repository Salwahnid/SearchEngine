import React from "react";

const SearchBar = ({ onSearch, placeholder, buttonText }) => {
  const [query, setQuery] = React.useState("");

  const handleSearch = () => {
    onSearch(query);
  };

  return (
    <div className="flex items-center space-x-4 p-4 bg-gray-100 rounded-lg shadow dark:bg-gray-800">
      <input
        type="text"
        placeholder={placeholder}
        className="flex-1 p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400 dark:bg-gray-700"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button
        className="px-4 py-2 text-white bg-blue-500 rounded hover:bg-blue-600"
        onClick={handleSearch}
      >
        {buttonText}
      </button>
    </div>
  );
};

export default SearchBar;
