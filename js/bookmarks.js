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

        container.innerHTML = '<p style="color: var(--text-muted);">Loading your library...</p>';

        const posts = await Bookmarks.getSavedPosts();
        const readPosts = await ReadingProgress.getReadPosts();
        const readSlugs = new Set(readPosts.map(p => p.post_slug));
        const emptyState = '<p id="empty-state" style="color: var(--text-muted); font-style: italic;">You haven\'t saved any posts yet. Go explore!</p>';

        if (posts.length === 0) {
            container.innerHTML = emptyState;
            return;
        }

        let html = '';
        posts.forEach(post => {
            const isRead = readSlugs.has(post.post_slug);
            const readBadge = isRead ? '<span class="read-badge">✓ Read</span>' : '';

            html += `
                <div class="saved-post-item">
                    <a href="posts/${post.post_slug}.html" class="post-card" style="border-bottom: none; padding: 1rem 0;">
                        <span class="post-meta">${post.post_category || 'General'} ${readBadge}</span>
                        <h2 style="margin-top: 0.5rem;">${post.post_title || 'Untitled'}</h2>
                    </a>
                    <div class="note-section">
                        <textarea 
                            class="note-input" 
                            placeholder="Add a note about this essay..."
                            data-post-id="${post.id}"
                            data-slug="${post.post_slug}"
                        >${post.notes || ''}</textarea>
                        <button class="save-note-btn" data-post-id="${post.id}">Save Note</button>
                    </div>
                </div>
            `;
        });

        container.innerHTML = html;

        // Add event listeners for save note buttons
        document.querySelectorAll('.save-note-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const postId = e.target.dataset.postId;
                const textarea = document.querySelector(`textarea[data-post-id="${postId}"]`);
                const note = textarea.value;

                const { error } = await supabaseClient
                    .from('user_bookmarks')
                    .update({ notes: note })
                    .eq('id', postId);

                if (!error) {
                    e.target.textContent = '✓ Saved';
                    e.target.style.backgroundColor = '#2e7d32';
                    setTimeout(() => {
                        e.target.textContent = 'Save Note';
                        e.target.style.backgroundColor = '';
                    }, 2000);
                }
            });
        });
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
