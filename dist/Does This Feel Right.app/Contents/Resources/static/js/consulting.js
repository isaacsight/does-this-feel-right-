document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('consulting-form');
    const successMsg = document.getElementById('form-success');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const submitBtn = form.querySelector('.submit-btn');
            const originalBtnText = submitBtn.textContent;
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;

            const formData = new FormData(form);
            const data = {
                name: formData.get('name'),
                email: formData.get('email'),
                message: formData.get('message')
            };

            try {
                const { error } = await window.supabaseClient
                    .from('leads')
                    .insert([data]);

                if (error) throw error;

                // Success
                form.style.display = 'none';
                successMsg.style.display = 'block';

            } catch (err) {
                console.error('Error submitting form:', err);
                submitBtn.textContent = 'Error. Try again.';
                submitBtn.disabled = false;
                alert('Failed to send message. Please try again or email me directly.');
            }
        });
    }
});
