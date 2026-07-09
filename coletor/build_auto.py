# -*- coding: utf-8 -*-
"""Construtor automático diário para publicação (GitHub Actions).

Fontes, por ordem de robustez:
  1. STJ — Dados Abertos (Temas.csv). Automático e completo. Sempre roda.
  2. STF — três camadas (coletor_stf.py), respeitando o robots.txt do portal:
       a) estoque oficial: arquivo 'stf-temas.csv' exportado do Painel de
          Repercussão Geral do Corte Aberta (exportação manual ocasional);
       b) novidades diárias por busca verificada via API da Anthropic
          (verificador_stf.py), ativada só quando houver ANTHROPIC_API_KEY;
       c) preservação: sem CSV e sem chave, a base anterior do STF fica intacta.
  3. Base curada (dados-manual.json: STF/TJMA/Súmulas verificados) — prioridade
     máxima, nunca apagada.

Cada fonte roda de forma isolada: se uma falhar num dia, as demais e a base
anterior seguem preservadas. Nunca se inventa conteúdo (regra de veracidade)."""
from util import log
import consolidar

def _seguro(nome, fn):
    try:
        return fn()
    except Exception as e:
        log(f"{nome}: indisponível hoje ({e}) — base anterior/curada preservada.")
        return []

def main():
    import coletor_stj, coletor_stf
    coletas = [
        _seguro("STJ", coletor_stj.coletar),
        _seguro("STF", coletor_stf.coletar),
    ]
    novos, alterados = consolidar.consolidar(coletas)
    log(f"Publicação preparada: {novos} novos, {alterados} alterados "
        f"(+ base curada sempre presente).")

if __name__ == "__main__":
    main()
