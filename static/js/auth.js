/**
 * Authentication using Supabase
 */

const Auth = {
    // Sign Up (New User)
    signUp: async (email, password) => {
        const { data, error } = await supabaseClient.auth.signUp({
            email: email,
            password: password,
        });
        return { data, error };
    },

    // Sign In (Existing User)
    signIn: async (email, password) => {
        const { data, error } = await supabaseClient.auth.signInWithPassword({
            email: email,
            password: password,
        });
        return { data, error };
    },

    // Sign Out
    logout: async () => {
        const { error } = await supabaseClient.auth.signOut();
        if (!error) {
            window.location.href = 'index.html';
        }
    },

    // Get Current User
    getUser: async () => {
        const { data: { user } } = await supabaseClient.auth.getUser();
        return user;
    },

    // Update UI based on Auth State
    updateUI: async () => {
        const user = await Auth.getUser();
        const authLink = document.getElementById('auth-link');

        if (authLink) {
            if (user) {
                authLink.textContent = 'My Library';
                const currentHref = authLink.getAttribute('href');
                // Replace login.html with library.html
                if (currentHref.includes('login.html')) {
                    authLink.href = currentHref.replace('login.html', 'library.html');
                }
            } else {
                authLink.textContent = 'Login';
                const currentHref = authLink.getAttribute('href');
                // Replace library.html with login.html
                if (currentHref.includes('library.html')) {
                    authLink.href = currentHref.replace('library.html', 'login.html');
                }
            }
        }

        // Handle Logout Button (only exists on Library page)
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                Auth.logout();
            });
        }
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    Auth.updateUI();

    // Handle Login Form
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const emailInput = document.getElementById('email');
            const passwordInput = document.getElementById('password'); // We need to add this to HTML
            const btn = loginForm.querySelector('button');
            const originalText = btn.textContent;

            if (!emailInput.value || !passwordInput.value) {
                alert('Please enter both email and password.');
                return;
            }

            btn.textContent = 'Signing in...';
            btn.disabled = true;

            // Try to Sign In first
            let { data, error } = await Auth.signIn(emailInput.value, passwordInput.value);

            if (error) {
                // If user doesn't exist (or wrong password), maybe try to sign up?
                // For simplicity in this prototype, let's just alert the error.
                // In a real app, we'd have separate Sign Up / Login flows.
                // Let's try to Sign Up if the error implies "Invalid login credentials" but we don't know if user exists.
                // Actually, let's just ask them to Sign Up if Login fails for now, or handle it explicitly.

                // Let's try to Sign Up automatically if Login fails (Lazy Registration)
                // WARNING: This is a bit hacky but good for prototypes.
                console.log("Login failed, trying signup...", error.message);
                const signUpResult = await Auth.signUp(emailInput.value, passwordInput.value);

                if (signUpResult.error) {
                    alert('Error: ' + signUpResult.error.message);
                    btn.textContent = originalText;
                    btn.disabled = false;
                } else {
                    alert('Account created! Please check your email to confirm.');
                    btn.textContent = originalText;
                    btn.disabled = false;
                }
            } else {
                // Success
                window.location.href = 'library.html';
            }
        });
    }
});
