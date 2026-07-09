-- ============================================================
-- Sistema de Precedentes — banco de perfis e sincronização
-- Execute UMA vez no SQL Editor do Supabase (projeto novo).
-- ============================================================

-- 1) Registros pessoais de cada usuário (um documento por perfil)
create table if not exists public.perfil_dados (
  user_id uuid primary key references auth.users(id) on delete cascade,
  dados jsonb not null,
  updated_at timestamptz not null default now()
);
alter table public.perfil_dados enable row level security;

create policy "perfil: ler o próprio"
  on public.perfil_dados for select
  using (auth.uid() = user_id);
create policy "perfil: criar o próprio"
  on public.perfil_dados for insert
  with check (auth.uid() = user_id);
create policy "perfil: atualizar o próprio"
  on public.perfil_dados for update
  using (auth.uid() = user_id);

-- 2) Papéis (o gestor é definido aqui, pelo e-mail)
create table if not exists public.papeis (
  email text primary key,
  papel text not null check (papel in ('gestor','usuario'))
);
alter table public.papeis enable row level security;
create policy "papeis: leitura por autenticados"
  on public.papeis for select
  using (auth.role() = 'authenticated');
-- Inclusões/alterações de papéis: apenas pelo painel do Supabase (gestor).

-- >>> AJUSTE AQUI: cadastre o e-mail do gestor <<<
insert into public.papeis (email, papel)
  values ('SEU-EMAIL-AQUI@exemplo.com', 'gestor')
  on conflict (email) do update set papel = excluded.papel;

-- 3) Observações compartilhadas do gabinete (uma por julgado)
create table if not exists public.notas_gabinete (
  julgado_id text primary key,
  texto text not null default '',
  autor_email text,
  updated_at timestamptz not null default now()
);
alter table public.notas_gabinete enable row level security;

create policy "gabinete: leitura por autenticados"
  on public.notas_gabinete for select
  using (auth.role() = 'authenticated');
create policy "gabinete: criar por autenticados"
  on public.notas_gabinete for insert
  with check (auth.role() = 'authenticated');
create policy "gabinete: atualizar por autenticados"
  on public.notas_gabinete for update
  using (auth.role() = 'authenticated');
create policy "gabinete: excluir apenas o gestor"
  on public.notas_gabinete for delete
  using (exists (select 1 from public.papeis p
                 where p.email = auth.jwt()->>'email' and p.papel = 'gestor'));
