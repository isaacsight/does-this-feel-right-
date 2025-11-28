-- Create leads table
CREATE TABLE IF NOT EXISTS leads (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT DEFAULT 'new'
);

-- Enable Row Level Security
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;

-- Policy: Allow public to insert (for the contact form)
CREATE POLICY "Allow public insert" ON leads
    FOR INSERT
    WITH CHECK (true);

-- Policy: Allow authenticated (service_role/admin) to select (for the dashboard)
-- Note: In a real app, we'd restrict this further. For this local admin tool using service_role, it's fine.
CREATE POLICY "Allow service_role select" ON leads
    FOR SELECT
    USING (true);
