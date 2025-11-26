-- Create the reactions table
create table reactions (
  slug text primary key,
  count int default 0
);

-- Enable Row Level Security
alter table reactions enable row level security;

-- Create a policy to allow anyone to read reactions
create policy "Enable read access for all users"
on reactions for select
using (true);

-- Create a policy to allow anyone to update (increment) reactions
-- Note: In a real production app, you might want a stored procedure to increment safely,
-- but for this MVP, direct update is fine if we trust the client not to set arbitrary values.
-- A safer way is to use a function.

create or replace function increment_reaction(post_slug text)
returns void as
$$
begin
  insert into reactions (slug, count)
  values (post_slug, 1)
  on conflict (slug)
  do update set count = reactions.count + 1;
end;
$$ language plpgsql;

-- Grant access to the function
grant execute on function increment_reaction(text) to anon, authenticated, service_role;

-- Allow anon to insert/update if we didn't use the function (optional, but function is better)
-- grant insert, update on reactions to anon;
