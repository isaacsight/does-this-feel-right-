// Theme handling
const themeToggle = {
    init: () => {
        // Check for saved theme or system preference
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

        if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
            document.documentElement.setAttribute('data-theme', 'dark');
        }

        // Add event listeners to toggles
        const toggles = document.querySelectorAll('.theme-toggle-btn');
        toggles.forEach(btn => {
            btn.addEventListener('click', themeToggle.toggle);
            themeToggle.updateIcon(btn);
        });
    },

    toggle: () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);

        // Update all toggle icons
        document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
            themeToggle.updateIcon(btn);
        });
    },

    updateIcon: (btn) => {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const sunIcon = btn.querySelector('.sun-icon');
        const moonIcon = btn.querySelector('.moon-icon');

        if (isDark) {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
        } else {
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
        }
    }
};

document.addEventListener('DOMContentLoaded', themeToggle.init);
