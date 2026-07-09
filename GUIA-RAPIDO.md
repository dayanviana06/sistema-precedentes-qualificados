# Guia rápido — colocar no ar em 4 passos (uma única vez)

Ao final, o senhor terá um site que se atualiza sozinho todos os dias, sem
nunca mais precisar mexer. Não é necessário instalar nada nem subir arquivos.

## Passo 1 — Criar o repositório a partir deste pacote
- Crie uma conta gratuita em github.com (se ainda não tiver).
- Crie um repositório novo (botão "New"), com visibilidade **Public**.
- Envie TODO o conteúdo desta pasta para o repositório (botão "Add file" →
  "Upload files" → arraste os arquivos e a pasta `coletor` e `.github`).

## Passo 2 — Ligar a publicação automática
- No repositório: aba **Settings** → **Pages**.
- Em "Build and deployment", no campo **Source**, escolha **GitHub Actions**.
- Pronto. Não escolha branch nem pasta; é só selecionar "GitHub Actions".

## Passo 3 — Ligar a atualização diária
- Aba **Actions** → se aparecer um aviso, clique em "I understand... enable".
- Abra o fluxo **"Atualizar e publicar"** → botão **Run workflow** para a
  primeira publicação imediata (nas próximas vezes é automático, às 6h).

## Passo 4 — Acessar
- Aguarde ~2 minutos. O endereço aparece em **Settings → Pages**
  (algo como `https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/`).
- Abra no computador ou no celular. No celular, use "Adicionar à tela inicial"
  para criar o ícone.

Está pronto. A partir daí:
- Todo dia, às 6h, o sistema baixa os precedentes qualificados do STJ
  (recursos repetitivos e IACs — de observância obrigatória) direto do Portal
  de Dados Abertos e republica o site sozinho.
- A base curada e verificada (temas do STF, IRDRs do TJMA, súmulas) está sempre
  presente e nunca é apagada.
- Cada pessoa que acessar tem seus próprios registros de estudo no navegador.

## E se eu quiser mais

Estes passos dão o essencial 100% automático. Os complementos abaixo são
OPCIONAIS e têm guias próprios neste pacote — não são necessários para o
sistema funcionar:
- **Acesso restrito** (só quem o senhor autorizar): `GUIA-ACESSO-RESTRITO.md`.
- **Nuvem do gabinete** (anotações entre dispositivos e observações
  compartilhadas): `GUIA-SINCRONIZACAO.md`.
- **Explicações por IA** (botão "💡 Explicar"): configure sua chave em
  ⚙ Configurações → Integração com o Claude, dentro do próprio aplicativo.
- **Informativos e planilha do STF**: exigem subir um arquivo e estão descritos
  no `LEIA-ME.md` (seção de informativos). Ficam de fora do fluxo automático
  justamente para não exigir trabalho manual recorrente.
