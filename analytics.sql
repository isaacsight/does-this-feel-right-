-- Create a table to track page views
create table if not exists public.page_views (
  slug text primary key,
  view_count bigint default 0,
  updated_at timestamp with time zone default timezone('utc'::text, now())
);

-- Enable Row Level Security (RLS)
alter table public.page_views enable row level security;

-- Allow anyone to read view counts (public)
create policy "Allow public read access"
  on public.page_views
  for select
  to public
  using (true);

-- Allow anyone to insert/update via the increment function (we'll restrict direct updates if needed, but for now RLS for update might block direct access)
-- Actually, for the RPC to work, we don't necessarily need update policies if the function is defined with `security definer`.

-- Create a function to atomically increment view count
create or replace function public.increment_page_view(page_slug text)
returns void
language plpgsql
security definer -- Runs with privileges of the creator (allows bypassing RLS for the update)
as $$
begin
  insert into public.page_views (slug, view_count, updated_at)
  values (page_slug, 1, now())
  on conflict (slug)
  do update set 
    view_count = page_views.view_count + 1,
    updated_at = now();
end;
$$;
