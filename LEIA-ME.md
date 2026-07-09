# Sistema de Precedentes Qualificados — STF · STJ · TJMA

> **Para começar rápido, leia o `GUIA-RAPIDO.md`.** Em 4 passos o site fica no
> ar e passa a se atualizar sozinho todos os dias, sem subir arquivos.

O restante deste documento detalha o funcionamento e os complementos opcionais.


Sistema completo: aplicativo de estudo, consulta e trabalho com sincronização
automática, alimentado por um coletor diário das fontes oficiais.

## O que está neste pacote

| Arquivo | Função |
|---|---|
| `precedentes-qualificados.html` | O aplicativo. Abre em qualquer navegador, funciona offline e sincroniza quando há internet (após configurar `DATA_URL`). |
| `dados.json` | Base de dados atual (semente verificada, 23 itens). É este arquivo que o coletor atualiza e o aplicativo baixa. |
| `dados-manual.json` | Curadoria do magistrado: tudo que constar aqui prevalece sobre a coleta automática. |
| `coletor/` | Coletor das três fontes (STJ, STF, TJMA), consolidador e camada didática opcional. |
| `.github/workflows/atualizar.yml` | Agendamento diário gratuito no GitHub Actions (06h de Brasília). |

## Instalação em 6 passos (uma única vez, ~15 minutos)

1. **Crie um repositório no GitHub** (pode ser privado só para o Actions; para o
   aplicativo sincronizar pela internet, o arquivo `dados.json` precisa ficar
   acessível — repositório público ou GitHub Pages).
2. **Envie todo o conteúdo deste pacote** para o repositório (arraste os arquivos
   na página "Add file → Upload files" do GitHub).
3. **Ative o agendamento**: aba *Actions* → habilite os workflows. O coletor
   passará a rodar todo dia às 06h (Brasília); também pode ser executado na hora
   pelo botão *Run workflow*.
4. **Publique a base**: *Settings → Pages → Deploy from branch → main → / (root)*.
   O endereço ficará: `https://SEU-USUARIO.github.io/NOME-DO-REPO/dados.json`.
5. **Aponte o aplicativo**: abra `precedentes-qualificados.html` em um editor de
   texto (Bloco de Notas serve), localize `const DATA_URL = ""` e cole o endereço
   do passo 4 entre as aspas. Salve.
6. **Instale no Windows**: abra o arquivo no Edge ou Chrome → menu → *Aplicativos*
   → *Instalar este site como aplicativo*. Ícone próprio, janela própria, funciona
   offline; sincroniza sozinho sempre que abrir com internet.

### Camada didática automática (opcional)
Para que os itens novos já cheguem com "Em suma" e explicação em linguagem
simples, cadastre em *Settings → Secrets and variables → Actions* o segredo
`ANTHROPIC_API_KEY`. Os textos gerados ficam marcados com `gerado_por_ia` e a IA
é proibida, por instrução, de citar qualquer norma ou dado que não conste da
tese oficial. Sem a chave, a etapa é simplesmente pulada.

## Site com ACESSO CONTROLADO (recomendado): Cloudflare Pages + Access

Para que somente pessoas autorizadas acessem o site de qualquer lugar, a
autenticação deve ocorrer ANTES de o conteúdo ser servido — nunca por "senha"
em JavaScript dentro da página, que é contornável. A solução gratuita e real:

1. **Repositório PRIVADO no GitHub** (nada fica público) com todo este pacote.
   O coletor diário (GitHub Actions) funciona normalmente em repositório privado.
2. **Cloudflare Pages** (conta gratuita): em *Workers & Pages → Create → Pages →
   Connect to Git*, conecte o repositório. A cada atualização do coletor, o site
   é republicado sozinho no endereço `https://SEU-PROJETO.pages.dev`.
3. **Cloudflare Access** (Zero Trust, gratuito até 50 usuários): em *Zero Trust →
   Access → Applications → Add an application → Self-hosted*, informe o domínio
   `SEU-PROJETO.pages.dev` e crie a política *Allow* com a lista de e-mails
   autorizados (*Include → Emails*). Ative o método de login *One-time PIN*:
   cada pessoa entra digitando o e-mail e o código que recebe — sem senhas para
   criar, guardar ou vazar.

**Papel de gestor**: o titular da conta Cloudflare (o senhor) é o gestor —
inclui e exclui e-mails autorizados no painel, a qualquer momento, com efeito
imediato; os registros de acesso ficam visíveis no painel do Zero Trust. O
aplicativo e o `dados.json` só são entregues a quem passou pelo login.

**Perfis dentro do aplicativo**: além do controle de acesso, o aplicativo tem
perfis locais (seletor 👤 na barra). O perfil **Gestor** cria e apaga perfis
para outras pessoas usarem o mesmo dispositivo com favoritos, leituras,
observações, cadernos e configurações totalmente isolados. Importante e
honesto: perfis locais organizam o uso compartilhado — quem BARRA estranhos é
o Cloudflare Access; e cada perfil guarda seus dados no navegador do próprio
dispositivo (migração entre máquinas pelo backup, nas Configurações).

O aplicativo publicado sincroniza sozinho com o `dados.json` do mesmo endereço
(mesma origem, já autenticada) — não é preciso configurar DATA_URL no site.

Cautelas que permanecem: nunca enviar arquivos de backup ao repositório (mesmo
privado, por higiene); ativar verificação em duas etapas no GitHub e na
Cloudflare; e lembrar que a versão em arquivo local continua funcionando
offline, mas, com o site protegido por login, ela não consegue sincronizar —
no site/celular, a sincronização é automática após o login.

## Nuvem do gabinete (sincronização entre dispositivos e observações compartilhadas)

Para que as anotações pessoais acompanhem o usuário em qualquer dispositivo e
para habilitar o mural de observações compartilhadas por julgado entre os
perfis do gabinete, siga o **GUIA-SINCRONIZACAO.md** (Supabase gratuito;
roteiro de banco pronto em `supabase-setup.sql`; gestor convida e remove os
perfis; login por código de e-mail; regras de segurança por linha garantem que
as anotações privadas permanecem privadas).

## Garantias de veracidade (por construção)

- Toda tese vem verbatim das fontes oficiais (Dados Abertos do STJ, página de
  Repercussão Geral do STF, fichas do NUGEPNAC/TJMA).
- O que o parser não conseguir extrair com segurança recebe o marcador
  `NAO_LOCALIZADO` — o sistema **nunca completa por suposição** e um valor
  `NAO_LOCALIZADO` **nunca sobrescreve** um dado anterior válido.
- Se uma fonte estiver fora do ar, as demais seguem e a base anterior daquela
  fonte é integralmente preservada.
- A camada didática já construída (resumos, mnemônicos, fluxogramas,
  dispositivos transcritos) **nunca é apagada** pela coleta.
- `changelog.json` registra, a cada rodada, o que entrou de novo e o que mudou.
- `dados-manual.json` dá a palavra final ao magistrado sobre qualquer item.

## O caso especial do STF (leia uma vez)

O portal do STF **bloqueia acesso automatizado** (robots.txt), inclusive a página
de teses e o site de notícias. Por isso o coletor do STF **não raspa página
nenhuma** — o que seria frágil e desrespeitaria a política do tribunal — e usa
duas vias legítimas:

1. **Estoque oficial (Corte Aberta).** O Painel de Repercussão Geral do programa
   Corte Aberta (Resolução STF 774/2022) tem a "Lista de temas" com exportação
   em CSV, feita para dados abertos. Uma vez (e depois quando quiser renovar):
   abra `https://transparencia.stf.jus.br/extensions/repercussao_geral/repercussao_geral.html`,
   exporte a Lista de Temas e salve o arquivo como `stf-temas.csv` na raiz do
   repositório. O coletor lê o CSV inteiro (todos os ~1.400 temas), com selos
   automáticos: tese vigente, "Pendente — mérito não julgado" e
   "Atenção — verificar" para cancelados/revisados.
2. **Novidades diárias por busca verificada.** Com o segredo `ANTHROPIC_API_KEY`
   cadastrado, o módulo `verificador_stf.py` usa a API da Anthropic **com busca
   na web** para localizar teses fixadas/alteradas nos últimos dias e revalidar
   temas pendentes — exigindo tese **verbatim** e a URL da fonte; qualquer
   incerteza vira `NAO_LOCALIZADO` (o código descarta textos curtos ou vagos).
   Itens assim obtidos ficam marcados `verificado_via: busca-ia`, com a fonte
   registrada no campo de situação, para conferência.

Sem o CSV e sem a chave, a base do STF simplesmente permanece como está — nada
se perde, nada se inventa.

## Informativos do STF e do STJ (a partir de 2020) — opcional

O sistema também ingere os informativos de jurisprudência, exibidos com o selo
próprio "Informativo" e marcados como **Consulta** (o informativo divulga
julgados; não é, por si, precedente vinculante — a vinculação segue restrita ao
rol do art. 927 do CPC). O corte temporal padrão é 2020 (ajustável em
`coletor/coletor_informativos.py`, constante `ANO_MINIMO`). Três vias:

1. **STF**: baixe a planilha oficial e estruturada do Informativo STF (todas as
   edições), divulgada pelo próprio Tribunal na página do Informativo, e salve
   como `stf-informativos.xlsx` na raiz do repositório.
2. **STJ (arquivo)**: exporte a pesquisa oficial de informativos e salve como
   `stj-informativos.csv` na raiz.
3. **STJ (automático)**: cole em `STJ_ESPELHOS_CSV` (`coletor/fontes.py`) as
   URLs de download dos Espelhos de Acórdãos do Portal de Dados Abertos
   (CSV, licença CC-BY) dos órgãos julgadores desejados — esta via atualiza
   sozinha, sem arquivo manual.

O aplicativo pagina automaticamente as áreas com muitos julgados ("Mostrar os
demais…"), de modo que o acervo de milhares de itens não pesa na leitura.

## Manutenção esperada

Quase nenhuma: (a) reexportar o `stf-temas.csv` do Corte Aberta quando desejar
renovar o estoque do STF (as novidades diárias já chegam pela busca verificada);
(b) acrescentar novas fichas do TJMA à lista `TJMA_FICHAS_PDF` em
`coletor/fontes.py`.
