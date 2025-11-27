-- Create the page_views table
create table page_views (
  slug text primary key,
  count int default 0,
  last_viewed_at timestamptz default now()
);

-- Enable Row Level Security
alter table page_views enable row level security;

-- Create a policy to allow anyone to read views (if we want to show them publicly later)
create policy "Enable read access for all users"
on page_views for select
using (true);

-- Create a function to safely increment view count
create or replace function increment_page_view(page_slug text)
returns void as
$$
begin
  insert into page_views (slug, count, last_viewed_at)
  values (page_slug, 1, now())
  on conflict (slug)
  do update set 
    count = page_views.count + 1,
    last_viewed_at = now();
end;
$$ language plpgsql;

-- Grant access to the function
grant execute on function increment_page_view(text) to anon, authenticated, service_role;
