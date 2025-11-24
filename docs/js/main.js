document.addEventListener('DOMContentLoaded', () => {
    // Newsletter Form Handling
    const forms = document.querySelectorAll('.newsletter-form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = form.querySelector('.newsletter-btn');
            const originalText = btn.textContent;

            btn.textContent = 'Subscribing...';
            btn.style.opacity = '0.7';

            // Simulate API call
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.opacity = '1';
                form.style.display = 'none';

                // Find the success message in the same container
                const successMsg = form.parentElement.querySelector('.success-message');
                if (successMsg) {
                    successMsg.style.display = 'block';
                }

                // Optional: Save to localStorage to remember subscription
                localStorage.setItem('isSubscribed', 'true');
            }, 1500);
        });
    });

    // Post Filtering Logic
    const filterBtns = document.querySelectorAll('.filter-btn');
    const posts = document.querySelectorAll('.post-card');

    if (filterBtns.length > 0) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // 1. Update Active State
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // 2. Filter Posts
                const filterValue = btn.getAttribute('data-filter');

                posts.forEach(post => {
                    if (filterValue === 'all' || post.getAttribute('data-category') === filterValue) {
                        post.style.display = 'block';
                    } else {
                        post.style.display = 'none';
                    }
                });
            });
        });
    }

    // Post Sorting Logic
    const sortBtns = document.querySelectorAll('.sort-btn');
    const postsContainer = document.querySelector('.posts-container');

    if (sortBtns.length > 0 && postsContainer) {
        sortBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();

                // Update active state
                sortBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const sortType = btn.getAttribute('data-sort');
                const postsArray = Array.from(posts);

                postsArray.sort((a, b) => {
                    if (sortType === 'date') {
                        const dateA = a.getAttribute('data-date') || '';
                        const dateB = b.getAttribute('data-date') || '';
                        return dateB.localeCompare(dateA); // newest first
                    } else if (sortType === 'title') {
                        const titleA = a.querySelector('h2').textContent;
                        const titleB = b.querySelector('h2').textContent;
                        return titleA.localeCompare(titleB);
                    }
                    return 0;
                });

                // Re-append in sorted order
                postsArray.forEach(post => postsContainer.appendChild(post));
            });
        });
    }

    // Mobile Menu Toggle
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navCenter = document.querySelector('.nav-center');

    if (mobileBtn && navCenter) {
        mobileBtn.addEventListener('click', () => {
            navCenter.classList.toggle('active');

            // Toggle icon between hamburger and X
            const isOpen = navCenter.classList.contains('active');
            if (isOpen) {
                mobileBtn.innerHTML = '<svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>';
            } else {
                mobileBtn.innerHTML = '<svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>';
            }
        });
    }
    // Search Toggle (handles both mobile and desktop)
    const searchBtns = document.querySelectorAll('.search-toggle-btn');
    const searchWrapper = document.querySelector('.search-wrapper');
    const searchInput = document.querySelector('#search-box');

    if (searchBtns.length > 0 && searchWrapper) {
        searchBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                searchWrapper.classList.toggle('active');

                // Auto-focus input when opened
                if (searchWrapper.classList.contains('active') && searchInput) {
                    setTimeout(() => searchInput.focus(), 100);
                }
            });
        });

        // Close search when clicking outside
        document.addEventListener('click', (e) => {
            if (!searchWrapper.contains(e.target) && !Array.from(searchBtns).some(btn => btn.contains(e.target))) {
                searchWrapper.classList.remove('active');
            }
        });
    }
});
