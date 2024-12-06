import React from "react";

const ResultsList = ({ results, noResultsText }) => {
  return (
    <div className="p-4">
      {results.length > 0 ? (
        results.map((doc, index) => (
          <div
            key={index}
            className="flex items-center p-4 mb-4 bg-white border rounded shadow hover:bg-gray-50 dark:bg-gray-800 "
          >
            <svg
              className="w-6 h-6 text-blue-500 mr-4"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z"
              />
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M14 2v6h6"
              />
            </svg>
            <div>
              <h3 className="text-lg font-semibold text-gray-800 dark:text-white">
                {doc.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-100">{doc.snippet}</p>
            </div>
          </div>
        ))
      ) : (
        <p className="text-gray-500">{noResultsText}</p>
      )}
    </div>
  );
};

export default ResultsList;
