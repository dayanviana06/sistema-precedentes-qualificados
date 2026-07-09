# -*- coding: utf-8 -*-
"""STF — coletor em três camadas (o portal do STF bloqueia robôs, então
não há raspagem direta; esta arquitetura respeita o robots.txt).

CAMADA 1 — Estoque oficial (arquivo local 'stf-temas.csv'):
  exportação da "Lista de temas" do Painel de Repercussão Geral do
  Corte Aberta (transparencia.stf.jus.br — programa oficial de dados
  abertos, Resolução STF 774/2022). Uma exportação manual de ~2 minutos
  carrega TODOS os temas; reexporte quando quiser renovar o estoque.

CAMADA 2 — Novidades diárias por busca verificada (verificador_stf.py):
  a API da Anthropic com a ferramenta de busca na web localiza teses
  fixadas/alteradas recentemente e as devolve VERBATIM com a fonte,
  sob regra de NAO_LOCALIZADO em caso de qualquer incerteza.

CAMADA 3 — Preservação: sem CSV e sem chave de API, a base anterior
  do STF permanece intacta (o consolidador nunca apaga nada)."""
import csv, io, os, re
from fontes import NAO_LOCALIZADO
from util import log

ARQUIVO_ESTOQUE = "stf-temas.csv"

def _norm(k):
    import unicodedata
    k = "".join(c for c in unicodedata.normalize("NFD", k or "")
                if unicodedata.category(c) != "Mn")
    return "".join(ch for ch in k.strip().lower() if ch.isalnum())

def _pega(r, *chaves):
    for c in chaves:
        if r.get(c):
            return r[c]
    return ""

def _validade(situacao, tese):
    s = (situacao or "").lower()
    if "cancelad" in s: return "Atenção — verificar"
    if "revis" in s:    return "Vigente — em revisão"
    if not tese or tese == NAO_LOCALIZADO: return "Pendente — mérito não julgado"
    return "Vigente"

def _ler_estoque():
    if not os.path.exists(ARQUIVO_ESTOQUE):
        log("STF: 'stf-temas.csv' ausente — camada de estoque pulada "
            "(exporte a Lista de Temas no Painel RG do Corte Aberta).")
        return []
    with open(ARQUIVO_ESTOQUE, encoding="utf-8-sig", errors="replace") as f:
        bruto = f.read()
    sep = ";" if bruto[:3000].count(";") > bruto[:3000].count(",") else ","
    leitor = csv.DictReader(io.StringIO(bruto), delimiter=sep)
    itens = []
    for row in leitor:
        r = {_norm(k): (v or "").strip() for k, v in row.items()}
        num = re.sub(r"\D", "", _pega(r, "tema", "numerotema", "numerodotema", "ntema"))
        if not num:
            continue
        tese = _pega(r, "tese", "tesefirmada", "tesederepercussaogeral")
        titulo = _pega(r, "titulo", "descricao", "descricaodotema", "assunto")
        situ = _pega(r, "situacao", "situacaodotema", "faseatual", "status")
        ramo = _pega(r, "ramododireito", "ramo", "materia") or "Repercussão Geral — STF"
        rel = _pega(r, "relator", "ministrorelator")
        itens.append({
            "id": f"stf-tema-{num}",
            "tribunal": "STF", "especie": "RG",
            "area": ramo, "obrigatorio": True,
            "validade": _validade(situ, tese),
            "situacao": situ or NAO_LOCALIZADO,
            "assuntos": [a for a in {ramo} if a],
            "numero": f"Tema {num}",
            "fonte": ("Corte Aberta/STF — Painel de Repercussão Geral"
                      + (f" — Rel. {rel}" if rel else "")),
            "titulo": (titulo[:180] or f"Tema {num} da Repercussão Geral"),
            "resumo": (tese or titulo or NAO_LOCALIZADO)[:400],
            "completo": tese or NAO_LOCALIZADO,
            "precedentes": _pega(r, "processo", "leadingcase", "processoparadigma"),
            "vinculos": [],
        })
    log(f"STF (estoque Corte Aberta): {len(itens)} temas lidos do CSV oficial.")
    return itens

def coletar():
    itens = _ler_estoque()
    try:
        import verificador_stf
        itens += verificador_stf.novidades()
    except Exception as e:
        log(f"STF (busca verificada): etapa indisponível ({e}) — sem prejuízo à base.")
    return itens
