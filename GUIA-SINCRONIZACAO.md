# Guia — Perfis com sincronização (Supabase)

Esta camada acrescenta ao aplicativo: login por código no e-mail (somente
usuários criados pelo gestor), sincronização automática dos registros pessoais
entre dispositivos e observações compartilhadas do gabinete. Camada gratuita
do Supabase; nenhum cartão de crédito é exigido. Sem esta configuração, o
aplicativo continua funcionando 100% local, como sempre.

## Instalação (uma vez, ~20 minutos)

1. Crie uma conta e um projeto em supabase.com (plano Free; escolha a região
   `South America (São Paulo)`).
2. **Banco**: menu *SQL Editor* → *New query* → cole o conteúdo integral de
   `supabase-setup.sql` (deste pacote) → antes de executar, substitua
   `SEU-EMAIL-AQUI@exemplo.com` pelo e-mail do gestor → *Run*.
3. **Login por código**: em *Authentication → Sign In / Up*, mantenha o
   provedor *Email* ativado e **desative** a opção de cadastro público
   (*Allow new users to sign up* = off). Assim, só entra quem o gestor criar.
4. **Credenciais do aplicativo**: em *Settings → API*, copie a *Project URL*
   e a *anon public key*.
5. **No aplicativo**: ⚙ Configurações → seção "☁ Nuvem" → cole a URL e a
   chave → *Salvar e conectar*.

## Perfis: como o gestor administra

- **Criar usuário**: painel do Supabase → *Authentication → Users → Add user*
  → informe o e-mail (não é preciso senha; o acesso é por código enviado ao
  e-mail). Pronto: a pessoa já consegue entrar pelo aplicativo.
- **Remover/suspender**: mesmo painel, excluir ou banir o usuário — o acesso
  cessa imediatamente.
- **Gestor**: o e-mail cadastrado na tabela `papeis` como `gestor` (passo 2).
  No aplicativo, é quem pode excluir observações do gabinete; no painel, é
  quem cria e remove usuários. Outros gestores: insira novas linhas na tabela.

## O que sincroniza

- **Registros pessoais** (leituras, revisões, observações próprias, cadernos,
  importados, favoritos e preferências): guardados por usuário, invisíveis aos
  demais (proteção por Row Level Security no banco), e sincronizados entre os
  dispositivos em que a pessoa fizer login — a ponte manual por backup deixa
  de ser necessária.
- **Observações do gabinete** (🏛): um campo compartilhado por julgado, visível
  e editável por todos os autenticados, com autor e data registrados; a
  exclusão é reservada ao gestor.

## Segurança e honestidades

- A *anon key* é pública por concepção; a proteção real está nas políticas de
  Row Level Security criadas pelo script — cada usuário só alcança os próprios
  dados, e o compartilhado exige autenticação.
- O login usa código de uso único no e-mail; não há senhas para vazar.
- Conflito entre dispositivos: vale a última gravação (o aplicativo envia as
  alterações ~2,5s após cada mudança). Para forçar, use "Recarregar da nuvem"
  ou "Enviar agora" nas Configurações.
- Camada gratuita do Supabase: 500 MB de banco e 50.000 usuários ativos/mês —
  ordens de grandeza acima do uso de um gabinete. Projetos gratuitos são
  pausados após ~7 dias sem uso e religados no painel em um clique; com uso
  diário do gabinete, isso não ocorre.
- Esta camada convive com o site restrito do GUIA-ACESSO-RESTRITO.md (a porta)
  e com a versão offline por arquivo: são camadas complementares.
