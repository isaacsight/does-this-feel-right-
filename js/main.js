document.addEventListener('DOMContentLoaded', () => {
    // Newsletter Form Handling
    // Newsletter Form Handling (ConvertKit Integration)
    const forms = document.querySelectorAll('.newsletter-form');
    forms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = form.querySelector('button[type="submit"]');
            const emailInput = form.querySelector('input[name="email_address"]');
            const originalText = btn.textContent;

            if (!emailInput || !emailInput.value) return;

            btn.textContent = 'Subscribing...';
            btn.style.opacity = '0.7';
            btn.disabled = true;

            try {
                const formData = new FormData();
                formData.append('email_address', emailInput.value);

                // ConvertKit Form ID: 8811203
                const response = await fetch('https://app.kit.com/forms/8811203/subscriptions', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json'
                    }
                });

                if (response.ok) {
                    const data = await response.json();

                    // Success UI
                    btn.textContent = '✓ Subscribed';
                    btn.style.backgroundColor = '#2e7d32';
                    btn.style.borderColor = '#2e7d32';

                    setTimeout(() => {
                        form.style.display = 'none';
                        // Find success message container (handle both sidebar and post layouts)
                        const container = form.closest('.newsletter-box') || form.closest('.newsletter-widget');
                        if (container) {
                            // Create or reveal success message
                            let successMsg = container.querySelector('.success-message');
                            if (!successMsg) {
                                successMsg = document.createElement('p');
                                successMsg.className = 'success-message';
                                successMsg.textContent = "You're on the list. Welcome.";
                                container.appendChild(successMsg);
                            }
                            successMsg.style.display = 'block';
                            successMsg.textContent = "Success! Check your email to confirm.";
                        }
                    }, 1000);

                    // Save state
                    localStorage.setItem('isSubscribed', 'true');
                } else {
                    throw new Error('Subscription failed');
                }
            } catch (error) {
                console.error('ConvertKit Error:', error);
                btn.textContent = 'Error. Try again.';
                btn.style.backgroundColor = '#d32f2f';
                btn.style.borderColor = '#d32f2f';

                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.backgroundColor = '';
                    btn.style.borderColor = '';
                    btn.style.opacity = '1';
                    btn.disabled = false;
                }, 3000);
            }
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
});
