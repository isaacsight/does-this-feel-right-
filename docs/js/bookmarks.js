/**
 * Bookmarking Logic using Supabase Database
 */

const Bookmarks = {
    // Fetch saved posts from Supabase
    getSavedPosts: async () => {
        const user = await Auth.getUser();
        if (!user) return [];

        const { data, error } = await supabaseClient
            .from('user_bookmarks')
            .select('*')
            .eq('user_id', user.id);

        if (error) {
            console.error('Error fetching bookmarks:', error);
            return [];
        }
        return data;
    },

    // Check if a specific slug is saved
    isSaved: async (slug) => {
        const user = await Auth.getUser();
        if (!user) return false;

        const { data, error } = await supabaseClient
            .from('user_bookmarks')
            .select('id')
            .eq('user_id', user.id)
            .eq('post_slug', slug)
            .single();

        return !!data;
    },

    // Toggle Save (Insert or Delete)
    toggleSave: async (postData) => {
        const user = await Auth.getUser();
        if (!user) return false;

        // Check if already saved
        const isSaved = await Bookmarks.isSaved(postData.slug);

        if (isSaved) {
            // Delete
            const { error } = await supabaseClient
                .from('user_bookmarks')
                .delete()
                .eq('user_id', user.id)
                .eq('post_slug', postData.slug);

            return !error ? false : true; // Return new state (false = not saved)
        } else {
            // Insert
            const { error } = await supabaseClient
                .from('user_bookmarks')
                .insert([
                    {
                        user_id: user.id,
                        post_slug: postData.slug,
                        post_title: postData.title, // Storing title/category denormalized for easier display
                        post_category: postData.category
                    }
                ]);

            return !error ? true : false; // Return new state (true = saved)
        }
    },

    renderLibrary: async () => {
        const container = document.getElementById('library-container');
        if (!container) return;

        // Show loading state?
        container.innerHTML = '<p style="color: var(--text-muted);">Loading your library...</p>';

        const posts = await Bookmarks.getSavedPosts();
        const emptyState = '<p id="empty-state" style="color: var(--text-muted); font-style: italic;">You haven\'t saved any posts yet. Go explore!</p>';

        if (posts.length === 0) {
            container.innerHTML = emptyState;
            return;
        }

        let html = '';
        posts.forEach(post => {
            // post_slug, post_title, post_category come from DB
            html += `
                <a href="posts/${post.post_slug}.html" class="post-card">
                    <span class="post-meta">${post.post_category || 'General'}</span>
                    <h2>${post.post_title || 'Untitled'}</h2>
                </a>
            `;
        });

        container.innerHTML = html;
    },

    initSaveButton: async () => {
        const btn = document.getElementById('save-btn');
        if (!btn) return;

        const slug = btn.dataset.slug;
        const title = btn.dataset.title;
        const category = btn.dataset.category;

        const updateBtnState = (saved) => {
            const textSpan = btn.querySelector('.text');
            if (saved) {
                textSpan.textContent = 'Saved';
                btn.style.opacity = '0.6';
            } else {
                textSpan.textContent = 'Save';
                btn.style.opacity = '1';
            }
        };

        // Initial State Check
        const saved = await Bookmarks.isSaved(slug);
        updateBtnState(saved);

        // Click Handler
        btn.addEventListener('click', async () => {
            const user = await Auth.getUser();
            if (!user) {
                alert('Please login to save posts.');
                window.location.href = '../login.html';
                return;
            }

            // Optimistic UI update
            const currentState = btn.querySelector('.text').textContent === 'Saved';
            updateBtnState(!currentState);

            const newState = await Bookmarks.toggleSave({ slug, title, category });

            // Verify state matches (in case of error)
            updateBtnState(newState);
        });
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    Bookmarks.initSaveButton();
    Bookmarks.renderLibrary();
});
