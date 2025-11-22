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
});
