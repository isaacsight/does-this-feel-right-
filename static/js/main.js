document.addEventListener('DOMContentLoaded', () => {
    // Newsletter Form Handling (Replaced by Substack Embeds)

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
    const mobileNavOverlay = document.querySelector('.mobile-nav-overlay');

    if (mobileBtn && mobileNavOverlay) {
        mobileBtn.addEventListener('click', () => {
            mobileNavOverlay.classList.toggle('active');

            // Toggle icon between hamburger and X
            const isOpen = mobileNavOverlay.classList.contains('active');
            if (isOpen) {
                mobileBtn.innerHTML = '<svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>';
            } else {
                mobileBtn.innerHTML = '<svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>';
            }
        });
    }

    // Support Button Logic (Scroll to bottom or open modal)
    const supportBtn = document.querySelector('.support-trigger');
    if (supportBtn) {
        supportBtn.addEventListener('click', () => {
            // For now, just scroll to footer or support section if it exists
            const supportSection = document.querySelector('.support-section');
            if (supportSection) {
                supportSection.scrollIntoView({ behavior: 'smooth' });
            } else {
                window.open('https://www.buymeacoffee.com/doesthisfeelright', '_blank');
            }
        });
    }

    // Welcome Gate Logic
    const welcomeGate = document.getElementById('welcome-gate');
    const enterBtn = document.getElementById('enter-site-btn');

    if (welcomeGate && enterBtn) {
        // Check if user has seen the gate
        const hasSeenGate = localStorage.getItem('hasSeenWelcomeGate');

        if (!hasSeenGate) {
            // Show gate
            welcomeGate.style.display = 'flex';
            document.body.style.overflow = 'hidden'; // Prevent scrolling

            enterBtn.addEventListener('click', () => {
                // Hide gate
                welcomeGate.style.opacity = '0';
                welcomeGate.style.transition = 'opacity 0.5s ease';

                setTimeout(() => {
                    welcomeGate.style.display = 'none';
                    document.body.style.overflow = ''; // Restore scrolling
                    localStorage.setItem('hasSeenWelcomeGate', 'true');
                }, 500);
            });
        }
    }
});
