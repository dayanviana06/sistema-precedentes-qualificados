# -*- coding: utf-8 -*-
"""TJMA — fichas oficiais do NUGEPNAC (PDF).
O parser segue a estrutura publicada nas fichas:
'Tese(s) Firmada(s):' … 'Processo(s) Paradigma(s):'."""
import io, re
from fontes import TJMA_FICHAS_PDF, NAO_LOCALIZADO
from util import baixar, log

def _texto_pdf(conteudo: bytes) -> str:
    from pypdf import PdfReader
    r = PdfReader(io.BytesIO(conteudo))
    return "\n".join((p.extract_text() or "") for p in r.pages)

CAMPOS = {
    "tema":      re.compile(r"TEMA\s+DO\s+IRDR\s*\(TJMA\)\s*:?\s*(\d+)", re.I),
    "tema_alt":  re.compile(r"TEMA\s*0?(\d+)\b", re.I),
    "titulo":    re.compile(r"TEMA\s+\d+\s*\n(.+?)\n", re.I),
    "situacao":  re.compile(r"Situa[cç][aã]o\s+do\s+Tema\s*:?\s*(.+?)(?:Data|Quest)", re.S | re.I),
    "questao":   re.compile(r"Quest[aã]o\s+Submetida\s+a\s+Julgamento\s*:?\s*(.+?)Tese", re.S | re.I),
    "teses":     re.compile(r"Tese\(s\)\s+Firmada\(s\)\s*:?\s*(.+?)Processo\(s\)\s+Paradigma", re.S | re.I),
    "relator":   re.compile(r"RELATOR\s*:?\s*(.+?)(?:DATA|\n)", re.S | re.I),
    "incidente": re.compile(r"N[ºo]\s+DO\s+INCIDENTE\s*\(TJMA\)\s*:?\s*([\d\.\-\s/()]+)", re.I),
}

def _campo(rx, txt):
    m = rx.search(txt)
    if not m:
        return NAO_LOCALIZADO
    return re.sub(r"\s+", " ", m.group(1)).strip()

def _validade(situacao):
    s = situacao.lower()
    if "revis" in s: return "Vigente — em revisão"
    if "cancel" in s or "superad" in s: return "Atenção — verificar"
    return "Vigente"

def parse_ficha(texto: str):
    tema = _campo(CAMPOS["tema"], texto)
    if tema == NAO_LOCALIZADO:
        tema = _campo(CAMPOS["tema_alt"], texto)
    teses = _campo(CAMPOS["teses"], texto)
    questao = _campo(CAMPOS["questao"], texto)
    situacao = _campo(CAMPOS["situacao"], texto)
    titulo = _campo(CAMPOS["titulo"], texto)
    if titulo == NAO_LOCALIZADO or len(titulo) < 8:
        titulo = (questao[:140] + "…") if questao != NAO_LOCALIZADO else f"IRDR — Tema {tema}/TJMA"
    if titulo.isupper():
        titulo = titulo.title()
    return {
        "id": f"tjma-irdr-{tema}" if tema != NAO_LOCALIZADO else None,
        "tribunal": "TJMA",
        "especie": "IRDR",
        "area": "Precedentes do TJMA",
        "obrigatorio": True,          # art. 927, III, e art. 985 do CPC
        "validade": _validade(situacao) if situacao != NAO_LOCALIZADO else "Vigente",
        "situacao": (f"Tema {tema}/TJMA — {situacao}"
                     if situacao != NAO_LOCALIZADO else NAO_LOCALIZADO),
        "assuntos": ["TJMA"],
        "numero": f"IRDR — Tema {tema}/TJMA",
        "fonte": ("Ficha oficial do NUGEPNAC/TJMA — Rel. " + _campo(CAMPOS["relator"], texto)
                  + " — Incidente " + _campo(CAMPOS["incidente"], texto)),
        "titulo": titulo,
        "resumo": (teses[:400] if teses != NAO_LOCALIZADO else questao[:400]),
        "completo": teses,
        "precedentes": "Ficha oficial do NUGEPNAC/TJMA",
        "vinculos": [],
    }

def coletar():
    itens = []
    for url in TJMA_FICHAS_PDF:
        try:
            log(f"TJMA: baixando ficha {url.rsplit('/', 1)[-1]}…")
            texto = _texto_pdf(baixar(url, binario=True))
            item = parse_ficha(texto)
            if item and item["id"]:
                itens.append(item)
            else:
                log("TJMA: ficha sem tema identificável — ignorada (nada inventado).")
        except Exception as e:
            log(f"TJMA: falha na ficha ({e}) — dados anteriores preservados.")
    log(f"TJMA: {len(itens)} temas coletados.")
    return itens
