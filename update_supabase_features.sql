-- Add reading history tracking
create table if not exists reading_history (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references auth.users not null,
  post_slug text not null,
  last_read_at timestamp with time zone default timezone('utc'::text, now()) not null,
  unique(user_id, post_slug)
);

-- Enable RLS
alter table reading_history enable row level security;

-- Policies for reading_history
create policy "Users can view their own reading history"
  on reading_history for select
  using ( auth.uid() = user_id );

create policy "Users can insert their own reading history"
  on reading_history for insert
  with check ( auth.uid() = user_id );

create policy "Users can update their own reading history"
  on reading_history for update
  using ( auth.uid() = user_id );

-- Add notes column to user_bookmarks
alter table user_bookmarks add column if not exists notes text;
