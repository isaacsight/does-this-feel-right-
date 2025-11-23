document.addEventListener('DOMContentLoaded', async () => {
    // Only run on post pages (check for the view-count element or URL pattern)
    const viewCountElement = document.getElementById('view-count');

    if (!viewCountElement) return;

    const slug = window.location.pathname.split('/').pop().replace('.html', '');

    if (!slug) return;

    try {
        // 1. Increment View Count
        // We use 'rpc' to call the stored procedure
        const { error: incrementError } = await supabase
            .rpc('increment_page_view', { page_slug: slug });

        if (incrementError) {
            console.error('Error incrementing view:', incrementError);
        }

        // 2. Fetch Updated Count
        const { data, error: fetchError } = await supabase
            .from('page_views')
            .select('view_count')
            .eq('slug', slug)
            .single();

        if (fetchError) {
            console.error('Error fetching view count:', fetchError);
            return;
        }

        if (data) {
            // Format number (e.g. 1,234)
            const formattedCount = new Intl.NumberFormat('en-US').format(data.view_count);
            viewCountElement.textContent = `${formattedCount} views`;
            viewCountElement.style.opacity = 1; // Fade in
        }

    } catch (err) {
        console.error('Analytics error:', err);
    }
});
