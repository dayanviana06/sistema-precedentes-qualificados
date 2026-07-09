# Guia — Site com acesso restrito (perfil de gestor e usuários autorizados)

Este guia converte o site em um ambiente fechado: só entra quem o gestor
autorizar, mediante login. Custo zero até 50 usuários. Nenhuma alteração no
aplicativo é necessária.

## Por que não basta uma senha no próprio site

O aplicativo é um arquivo estático: qualquer senha colocada dentro dele fica
visível no código-fonte e é contornável. Segurança real exige autenticação
ANTES de o navegador receber a página. É o que o Cloudflare Access faz: ele se
posiciona na frente do site e só entrega o conteúdo após verificar a identidade
do visitante.

## Arquitetura recomendada

1. **Repositório PRIVADO no GitHub** — o coletor diário continua funcionando
   normalmente em repositório privado (o plano gratuito inclui 2.000 minutos
   mensais de automação; o coletor consome ~2 minutos por dia). Com o
   repositório privado, nem o código nem o `dados.json` ficam expostos.
2. **Cloudflare Pages** conectado a esse repositório — publica o site
   automaticamente a cada atualização (inclusive a atualização diária do
   `dados.json` feita pelo coletor). Gratuito.
3. **Cloudflare Zero Trust (Access)** na frente do site — exige login e aplica
   a lista de autorizados definida pelo gestor. Gratuito até 50 usuários.

Resultado: endereço próprio (ex.: `precedentes.pages.dev`), acessível de
qualquer lugar e dispositivo, mas somente para quem estiver na lista.

## Passo a passo (uma única vez, ~25 minutos)

**A. Repositório privado**
1. No GitHub, crie o repositório como *Private* (ou converta o existente em
   *Settings → General → Danger Zone → Change visibility*).
2. Envie o conteúdo do pacote (inclusive `index.html` e `dados.json`).
3. Ative os *Actions* (aba Actions) — o coletor diário passa a rodar.

**B. Publicação (Cloudflare Pages)**
4. Crie uma conta gratuita em cloudflare.com.
5. Painel → *Workers & Pages* → *Create* → *Pages* → *Connect to Git* →
   autorize o GitHub e selecione o repositório.
6. Configurações de build: deixe tudo em branco (framework "None", build
   command vazio, output "/") — é um site estático puro. Conclua o deploy.
7. Anote o endereço gerado (ex.: `https://precedentes-xxx.pages.dev`).

**C. Fechadura (Cloudflare Access)**
8. Painel → *Zero Trust* (primeiro acesso pede a criação de um "team name" e a
   escolha do plano **Free**).
9. *Access → Applications → Add an application → Self-hosted*.
10. Em *Application domain*, selecione o domínio `.pages.dev` do passo 7
    (subdomínio: o nome do projeto; caminho: deixe vazio para proteger tudo,
    inclusive o `dados.json`).
11. Crie a política de acesso (o coração dos "perfis"):
    - Nome: `Autorizados`
    - Action: `Allow`
    - Include → `Emails` → liste os e-mails autorizados (o seu e os da equipe).
12. Método de login: por padrão, *One-time PIN* — a pessoa digita o e-mail,
    recebe um código de uso único e entra. Não há senhas para criar, perder ou
    vazar. (Opcional: adicionar login pelo Google em *Settings →
    Authentication*.)

## Como funcionam os perfis, na prática

- **Gestor** = quem controla a conta Cloudflare (o senhor). Somente o gestor
  inclui, remove ou suspende autorizados — basta editar a lista de e-mails da
  política; a revogação vale imediatamente, sem tocar no site.
- **Usuários** = cada e-mail autorizado. Cada pessoa entra com o próprio
  e-mail; o Access registra os acessos (*Zero Trust → Logs*), permitindo ao
  gestor auditar quem entrou e quando.
- **Dados pessoais de estudo** (observações, cadernos, leituras, revisões)
  continuam, por construção, no navegador de cada pessoa: um usuário jamais vê
  as anotações de outro. O site entrega o mesmo acervo a todos; o estudo é
  individual em cada dispositivo.
- Sessão: o Access mantém o login pelo período definido pelo gestor
  (padrão 24h; ajustável na aplicação).

## Ajuste único no aplicativo

Dentro do site, abra **⚙ Configurações → Sincronização** e preencha o endereço
com simplesmente `dados.json` (caminho relativo). Assim a base é servida pelo
mesmo endereço protegido — quem não estiver autorizado não obtém nem o
aplicativo nem os dados.

## Limites e honestidades

- O plano gratuito comporta 50 usuários — muito além de um gabinete.
- O celular acessa normalmente (login por código no e-mail) e pode fixar o
  ícone na tela inicial; para uso 100% offline, a versão por arquivo instalada
  no computador continua disponível e independente.
- O conteúdo protegido é o acervo e o aplicativo; vale lembrar que a
  jurisprudência em si é pública — a restrição atende à prudência
  institucional, não a um sigilo legal do conteúdo.
- Se, no futuro, desejar perfis com **sincronização das anotações entre
  dispositivos e entre usuários** (por exemplo, observações compartilhadas do
  gabinete), isso exige um banco de dados com autenticação (Firebase/Supabase,
  também com camadas gratuitas) e uma evolução do aplicativo — é o passo
  seguinte natural, não incluído nesta etapa.
