/**
 * Search functionality
 */

const Search = {
    init: () => {
        const searchBox = document.getElementById('search-box');
        if (!searchBox) return;

        searchBox.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const postCards = document.querySelectorAll('.post-card');

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
        });
    }
};

// Initialize on homepage
if (document.getElementById('search-box')) {
    Search.init();
}
