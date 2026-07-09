# Como ativar os precedentes do STF (automático)

O sistema já coleta o STJ sozinho. Este guia ativa também o STF, de forma
automática, no mesmo fluxo diário. São dois níveis — o primeiro já resolve a
maior parte; o segundo deixa tudo no piloto automático.

---

## Por que o STF exige um passo a mais que o STJ

O STJ publica um arquivo oficial de dados abertos que qualquer programa pode
baixar. O STF não tem esse arquivo: o portal dele bloqueia acesso automatizado
(regra do próprio Tribunal), e os temas de repercussão geral só saem por
exportação no painel Corte Aberta. Por isso o STF é coletado em camadas, todas
já programadas — o senhor só precisa alimentar a primeira uma vez.

---

## Nível 1 — Carga inicial do STF (uma vez, ~2 minutos)

1. Acesse o Painel de Repercussão Geral do Corte Aberta:
   https://transparencia.stf.jus.br/extensions/repercussao_geral/repercussao_geral.html
2. Vá à aba **"Lista de temas"**.
3. No canto inferior direito do painel, use o botão de **exportar** e escolha
   **CSV** (ou Excel, que depois se salva como CSV).
4. Renomeie o arquivo para exatamente **`stf-temas.csv`**.
5. Coloque esse arquivo na **pasta raiz do repositório** (a mesma onde estão
   `index.html` e `dados.json`) e envie ao GitHub.

Pronto. Na próxima execução (diária ou pelo botão "Run workflow"), todos os
temas do STF entram na base, com tese, situação e relator, ao lado do STJ.

> Para renovar o estoque do STF no futuro, repita a exportação e substitua o
> `stf-temas.csv`. Não precisa ser frequente: as **novidades** entre uma
> exportação e outra são cobertas pelo Nível 2.

---

## Nível 2 — Novidades diárias do STF no piloto automático (opcional)

Este nível faz o sistema buscar, todo dia, os temas do STF cuja tese foi
fixada ou alterada recentemente — sem o senhor exportar nada de novo. Ele usa
uma verificação por busca na web, com regra estrita de veracidade: só grava a
tese se localizar o texto oficial; na dúvida, marca como pendente, nunca inventa.

Para ativar, cadastre uma chave da API da Anthropic como segredo do repositório:

1. No GitHub, abra o repositório e vá em **Settings → Secrets and variables →
   Actions → New repository secret**.
2. Nome: **`ANTHROPIC_API_KEY`**
3. Valor: sua chave (formato `sk-ant-...`), obtida em https://console.anthropic.com
4. Salve.

A partir daí, o fluxo diário passa a incluir as novidades verificadas do STF.
Sem essa chave, o sistema continua funcionando normalmente com o Nível 1 — a
chave só acrescenta a atualização automática entre exportações.

---

## O que acontece se algo falhar num dia

Cada fonte roda isolada. Se o STJ estiver fora do ar, o STF e a base curada
seguem. Se o `stf-temas.csv` não estiver presente, o STF usa o que já havia na
base. Nada é apagado e nada é inventado — a base só cresce e se corrige com
fontes verificadas.
