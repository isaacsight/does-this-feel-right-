-- 1. Create table if it doesn't exist
create table if not exists page_views (
  slug text primary key,
  count int default 0,
  last_viewed_at timestamptz default now()
);

-- 2. Enable RLS (Safe to run, idempotent)
alter table page_views enable row level security;

-- 3. Policy (Drop and recreate to be safe)
drop policy if exists "Enable read access for all users" on page_views;
create policy "Enable read access for all users"
on page_views for select
using (true);

-- 4. Function (Replace is already idempotent)
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

-- 5. Grant access
grant execute on function increment_page_view(text) to anon, authenticated, service_role;
