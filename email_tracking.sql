-- Track which posts have been sent via email
create table if not exists email_notifications (
  id uuid default uuid_generate_v4() primary key,
  post_slug text not null,
  sent_at timestamp with time zone default timezone('utc'::text, now()) not null,
  recipient_count integer default 0,
  unique(post_slug)
);

-- No RLS needed - admin only table
