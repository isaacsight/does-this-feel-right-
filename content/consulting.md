---
title: Consulting
category: Services
excerpt: Let's fix your problem.
---

<div style="font-family: var(--font-serif); max-width: 600px; margin: 0 auto;">

<h1 style="font-size: 2.5rem; margin-bottom: 1rem; line-height: 1.2;">Let’s Fix Your Problem.</h1>

<p style="font-size: 1.2rem; color: var(--text-muted); margin-bottom: 3rem; line-height: 1.6;">
    Tell me who you are, how to reach you, and what you’re stuck on. I’ll take it from there.
</p>

<form id="consulting-form" style="display: flex; flex-direction: column; gap: 1.5rem;">
    <div class="form-group">
        <label for="name" style="display: block; font-weight: 600; margin-bottom: 0.5rem; font-family: var(--font-sans); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">Name</label>
        <input type="text" id="name" name="name" required 
            style="width: 100%; padding: 1rem; border: 1px solid var(--border-color); background: var(--bg-color); font-family: var(--font-sans); font-size: 1rem; border-radius: 4px;">
    </div>

    <div class="form-group">
        <label for="email" style="display: block; font-weight: 600; margin-bottom: 0.5rem; font-family: var(--font-sans); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">Email</label>
        <input type="email" id="email" name="email" required 
            style="width: 100%; padding: 1rem; border: 1px solid var(--border-color); background: var(--bg-color); font-family: var(--font-sans); font-size: 1rem; border-radius: 4px;">
    </div>

    <div class="form-group">
        <label for="problem" style="display: block; font-weight: 600; margin-bottom: 0.5rem; font-family: var(--font-sans); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">Your Problem (tell me what’s going on):</label>
        <textarea id="problem" name="problem" rows="6" placeholder="Write as much or as little as you want." required
            style="width: 100%; padding: 1rem; border: 1px solid var(--border-color); background: var(--bg-color); font-family: var(--font-sans); font-size: 1rem; line-height: 1.6; border-radius: 4px; resize: vertical;"></textarea>
    </div>

    <button type="submit" id="submit-btn"
        style="background: var(--text-main); color: var(--panel-bg); border: none; padding: 1.2rem 2rem; font-size: 1rem; font-weight: 600; cursor: pointer; border-radius: 4px; font-family: var(--font-sans); margin-top: 1rem; transition: opacity 0.2s;">
        Submit Problem
    </button>
    
    <p id="form-status" style="margin-top: 1rem; font-style: italic; display: none;"></p>
</form>

</div>

<script>
document.getElementById('consulting-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('submit-btn');
    const status = document.getElementById('form-status');
    const originalText = btn.textContent;
    
    btn.textContent = 'Sending...';
    btn.disabled = true;
    
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        problem: document.getElementById('problem').value,
        timestamp: new Date().toISOString()
    };

    try {
        // Use Supabase to insert
        const { error } = await window.supabaseClient
            .from('consulting_leads')
            .insert([formData]);

        if (error) throw error;

        status.textContent = "Received. I'll be in touch shortly.";
        status.style.color = 'var(--accent-success)';
        status.style.display = 'block';
        btn.style.display = 'none';
        
    } catch (err) {
        console.error('Error:', err);
        // Fallback to mailto if Supabase fails or table doesn't exist yet
        window.location.href = `mailto:isaac@doesthisfeelright.com?subject=Consulting Inquiry: ${formData.name}&body=${encodeURIComponent(formData.problem)}%0A%0AFrom: ${formData.email}`;
        
        status.textContent = "Opening your email client...";
        status.style.display = 'block';
        btn.textContent = originalText;
        btn.disabled = false;
    }
});
</script>
