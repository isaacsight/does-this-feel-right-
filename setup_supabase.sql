-- Create a table for User Bookmarks
create table user_bookmarks (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references auth.users not null,
  post_slug text not null,
  post_title text,
  post_category text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  unique(user_id, post_slug)
);

-- Enable Row Level Security (RLS)
alter table user_bookmarks enable row level security;

-- Create Policy: Users can only see their own bookmarks
create policy "Users can view their own bookmarks"
  on user_bookmarks for select
  using ( auth.uid() = user_id );

-- Create Policy: Users can insert their own bookmarks
create policy "Users can insert their own bookmarks"
  on user_bookmarks for insert
  with check ( auth.uid() = user_id );

-- Create Policy: Users can delete their own bookmarks
create policy "Users can delete their own bookmarks"
  on user_bookmarks for delete
  using ( auth.uid() = user_id );
