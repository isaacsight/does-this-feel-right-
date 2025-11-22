document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('.newsletter-form');

    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const container = form.closest('.newsletter-box');
            const successMsg = container.querySelector('.success-message');
            const input = form.querySelector('.newsletter-input');
            const button = form.querySelector('.newsletter-btn');
            
            // Simulate API call
            button.textContent = 'Subscribing...';
            button.disabled = true;
            input.disabled = true;

            setTimeout(() => {
                form.style.display = 'none';
                successMsg.style.display = 'block';
                
                // Optional: Save to local storage
                localStorage.setItem('subscribed', 'true');
            }, 800);
        });
    });
});
