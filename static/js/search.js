/**
 * Search functionality
 */

const Search = {
    init: () => {
        const searchInputs = document.querySelectorAll('#header-search, #mobile-search');
        if (searchInputs.length === 0) return;

        const handleSearch = (query) => {
            const postCards = document.querySelectorAll('.post-card');

            // Sync inputs
            searchInputs.forEach(input => {
                if (input.value !== query) input.value = query;
            });

            postCards.forEach(card => {
                const title = card.querySelector('h2')?.textContent.toLowerCase() || '';
                const excerpt = card.querySelector('.post-excerpt')?.textContent.toLowerCase() || '';
                const category = card.querySelector('.post-meta')?.textContent.toLowerCase() || '';

                const matches = title.includes(query) || excerpt.includes(query) || category.includes(query);

                if (matches || query === '') {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        };

        searchInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                handleSearch(e.target.value.toLowerCase());
            });
        });
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    Search.init();
});
