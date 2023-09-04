document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const resultsContainer = document.getElementById('results-container');

    searchButton.addEventListener('click', () => {
        const searchTerm = searchInput.value.trim();

        if (searchTerm !== '') {
            // Send a POST request to the server
            fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ search_term: searchTerm }),
            })
            .then(response => response.json())
            .then(data => {
                // Process and display the search results
                displayResults(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });

    function displayResults(results) {
        resultsContainer.innerHTML = '';

        results.forEach(result => {
            const resultItem = document.createElement('div');
            resultItem.textContent = result.content;
            resultsContainer.appendChild(resultItem);
        });
    }
});
