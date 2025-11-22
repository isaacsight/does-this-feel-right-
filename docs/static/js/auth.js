/**
 * Authentication using Supabase - Improved UX
 */

const Auth = {
    // Sign Up (New User)
    signUp: async (email, password) => {
        const { data, error } = await supabaseClient.auth.signUp({
            email: email,
            password: password,
            options: {
                emailRedirectTo: window.location.origin + '/library.html'
            }
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
                if (currentHref.includes('login.html')) {
                    authLink.href = currentHref.replace('login.html', 'library.html');
                }
            } else {
                authLink.textContent = 'Login';
                const currentHref = authLink.getAttribute('href');
                if (currentHref.includes('library.html')) {
                    authLink.href = currentHref.replace('library.html', 'login.html');
                }
            }
        }

        // Handle Logout Button
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
        const messageEl = document.getElementById('login-message');

        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const emailInput = document.getElementById('email');
            const passwordInput = document.getElementById('password');
            const btn = loginForm.querySelector('button');
            const originalText = btn.textContent;

            if (!emailInput.value || !passwordInput.value) {
                if (messageEl) {
                    messageEl.style.display = 'block';
                    messageEl.style.color = '#d32f2f';
                    messageEl.textContent = 'Please enter both email and password.';
                }
                return;
            }

            if (passwordInput.value.length < 6) {
                if (messageEl) {
                    messageEl.style.display = 'block';
                    messageEl.style.color = '#d32f2f';
                    messageEl.textContent = 'Password must be at least 6 characters.';
                }
                return;
            }

            btn.textContent = 'Signing in...';
            btn.disabled = true;

            // Try to Sign In first
            let { data, error } = await Auth.signIn(emailInput.value, passwordInput.value);

            if (error && error.message.includes('Invalid login credentials')) {
                // User doesn't exist, try to sign up
                btn.textContent = 'Creating account...';
                const signUpResult = await Auth.signUp(emailInput.value, passwordInput.value);

                if (signUpResult.error) {
                    if (messageEl) {
                        messageEl.style.display = 'block';
                        messageEl.style.color = '#d32f2f';
                        messageEl.textContent = 'Error: ' + signUpResult.error.message;
                    }
                    btn.textContent = originalText;
                    btn.disabled = false;
                } else {
                    // Check if email confirmation is required
                    if (signUpResult.data.user && !signUpResult.data.session) {
                        if (messageEl) {
                            messageEl.style.display = 'block';
                            messageEl.style.color = '#2e7d32';
                            messageEl.textContent = '✓ Account created! Check your email to confirm, then come back to log in.';
                        }
                        btn.textContent = originalText;
                        btn.disabled = false;
                    } else {
                        // No email confirmation needed, sign in was successful
                        if (messageEl) {
                            messageEl.style.display = 'block';
                            messageEl.style.color = '#2e7d32';
                            messageEl.textContent = '✓ Welcome! Redirecting...';
                        }
                        setTimeout(() => {
                            window.location.href = 'library.html';
                        }, 1000);
                    }
                }
            } else if (error) {
                if (messageEl) {
                    messageEl.style.display = 'block';
                    messageEl.style.color = '#d32f2f';
                    messageEl.textContent = 'Error: ' + error.message;
                }
                btn.textContent = originalText;
                btn.disabled = false;
            } else {
                // Success
                if (messageEl) {
                    messageEl.style.display = 'block';
                    messageEl.style.color = '#2e7d32';
                    messageEl.textContent = '✓ Welcome back! Redirecting...';
                }
                setTimeout(() => {
                    window.location.href = 'library.html';
                }, 1000);
            }
        });
    }
});
