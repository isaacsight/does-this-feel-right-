/**
 * Reading Progress Tracker
 */

const ReadingProgress = {
    // Mark a post as read
    markAsRead: async (slug) => {
        const user = await Auth.getUser();
        if (!user) return;

        const { error } = await supabaseClient
            .from('reading_history')
            .upsert({
                user_id: user.id,
                post_slug: slug,
                last_read_at: new Date().toISOString()
            }, {
                onConflict: 'user_id,post_slug'
            });

        if (error) console.error('Error marking as read:', error);
    },

    // Check if a post was read
    isRead: async (slug) => {
        const user = await Auth.getUser();
        if (!user) return false;

        const { data } = await supabaseClient
            .from('reading_history')
            .select('id')
            .eq('user_id', user.id)
            .eq('post_slug', slug)
            .single();

        return !!data;
    },

    // Get all read posts
    getReadPosts: async () => {
        const user = await Auth.getUser();
        if (!user) return [];

        const { data } = await supabaseClient
            .from('reading_history')
            .select('post_slug, last_read_at')
            .eq('user_id', user.id);

        return data || [];
    },

    // Initialize tracking on post pages
    initPostTracking: () => {
        // Only track on post pages (not index, about, login, library)
        const path = window.location.pathname;
        if (!path.includes('/posts/')) return;

        // Extract slug from URL
        const slug = path.split('/posts/')[1]?.replace('.html', '');
        if (!slug) return;

        // Mark as read after 5 seconds of being on the page
        setTimeout(async () => {
            await ReadingProgress.markAsRead(slug);
        }, 5000);
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    ReadingProgress.initPostTracking();
});
