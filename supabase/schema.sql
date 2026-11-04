-- Caja Negra: resultados compartidos entre todos los equipos.
-- Pega este archivo en Supabase > SQL Editor y ejecútalo una vez.
--
-- El juego usa una clave pública, visible en el código de la página. Por eso
-- quien la tenga solo puede leer y agregar filas: ni editarlas ni borrarlas.
-- Las restricciones de cada columna también protegen la página, que muestra
-- estos valores en el tablero. No las quites sin revisar renderTablero.

create table if not exists public.partidas (
  id         uuid primary key,
  decision   text check (decision in ('GO', 'COND', 'NOGO')),
  verif_text text check (char_length(verif_text) <= 1000),
  modo       text check (modo in ('individual', 'sala')),
  pub        smallint check (pub between 0 and 6),
  priv       smallint check (priv between 0 and 6),
  hidden     smallint check (hidden between 0 and 6),
  outcome    text check (outcome in ('success', 'failure', 'aborted', 'none')),
  risk       numeric check (risk between 0 and 100),
  jugada_en  timestamptz not null,
  creada_en  timestamptz not null default now()
);

create table if not exists public.muro (
  id        uuid primary key,
  texto     text not null check (char_length(texto) between 1 and 500),
  creada_en timestamptz not null default now()
);

create index if not exists partidas_jugada_en_idx on public.partidas (jugada_en);
create index if not exists muro_creada_en_idx on public.muro (creada_en desc);

alter table public.partidas enable row level security;
alter table public.muro enable row level security;

revoke all on public.partidas, public.muro from anon, authenticated;
grant select, insert on public.partidas, public.muro to anon;

drop policy if exists "leer partidas" on public.partidas;
create policy "leer partidas" on public.partidas for select to anon using (true);
drop policy if exists "agregar partidas" on public.partidas;
create policy "agregar partidas" on public.partidas for insert to anon with check (true);

drop policy if exists "leer muro" on public.muro;
create policy "leer muro" on public.muro for select to anon using (true);
drop policy if exists "agregar al muro" on public.muro;
create policy "agregar al muro" on public.muro for insert to anon with check (true);
