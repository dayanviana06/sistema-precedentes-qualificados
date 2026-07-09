# -*- coding: utf-8 -*-
"""STJ — Dados Abertos: Temas.csv dos Precedentes Qualificados.
Esquema REAL do arquivo (verificado no dicionário oficial e em amostra em
07/2026): colunas numeroPrecedente, tipoPrecedente, teseFirmada,
questaoSubmetidaAJulgamento, situacao, Assuntos (taxonomia CNJ:
"1156- DIREITO DO CONSUMIDOR, 7771- Contratos de Consumo, ..."),
orgaoJulgador, dataJulgamento, sumulaOriginada, numeroRepercussaoGeralSTF.

A MATÉRIA de cada tema é o ramo em MAIÚSCULAS dos Assuntos; os demais itens
viram assuntos filtráveis. Tipos incluídos: Tema Repetitivo e IAC
(vinculantes, art. 927, III, CPC), PUIL e SIRDR (qualificados, consulta).
'Controvérsia' é etapa administrativa pré-afetação e fica de fora."""
import csv, io, re
from fontes import STJ_TEMAS_CSV, NAO_LOCALIZADO
from util import baixar, log

def _norm(k):
    import unicodedata
    k = "".join(c for c in unicodedata.normalize("NFD", str(k or ""))
                if unicodedata.category(c) != "Mn")
    return "".join(ch for ch in k.strip().lower() if ch.isalnum())

def _limpa(s, max_len=None):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s[:max_len] if max_len else s

def parse_assuntos(bruto):
    """'1156- DIREITO DO CONSUMIDOR, 7771- Contratos de Consumo' →
       (matéria='Direito do Consumidor', assuntos=[...ramos e subtemas...])"""
    partes = [re.sub(r"^\s*\d+\s*-\s*", "", p).strip()
              for p in str(bruto or "").split(",")]
    partes = [p for p in partes if p]
    ramos, subs = [], []
    for p in partes:
        letras = re.sub(r"[^A-Za-zÀ-ÿ]", "", p)
        if letras and letras.upper() == letras and len(letras) > 3:
            ramos.append(p.title().replace(" E ", " e ").replace(" Do ", " do ")
                          .replace(" Da ", " da ").replace(" De ", " de "))
        else:
            subs.append(p)
    materia = ramos[0] if ramos else "Precedentes do STJ"
    assuntos = ramos + subs
    return materia, assuntos

def _especie(tipo):
    t = (tipo or "").lower()
    if "repetitivo" in t: return "REP", True
    if "assun" in t or "iac" in t: return "IAC", True
    if "puil" in t or "uniformiza" in t: return "PUIL", True
    if "sirdr" in t or "suspens" in t: return "SIRDR", False
    return None, False   # Controvérsia e demais: não entram

def _validade(situacao, tese):
    s = (situacao or "").lower()
    if "cancelad" in s: return "Atenção — verificar"
    if "revis" in s: return "Vigente — em revisão"
    if not tese: return "Pendente — mérito não julgado"
    return "Vigente"

def coletar():
    log("STJ: baixando Temas.csv (dados abertos)…")
    bruto = baixar(STJ_TEMAS_CSV)
    if bruto.startswith("\ufeff"):
        bruto = bruto.lstrip("\ufeff")
    leitor = csv.DictReader(io.StringIO(bruto))   # separador real: vírgula, campos com aspas
    itens, ramos_vistos = [], set()
    for row in leitor:
        r = {_norm(k): (v or "") for k, v in row.items()}
        esp, obrig = _especie(r.get("tipoprecedente"))
        if not esp:
            continue
        num = _limpa(r.get("numeroprecedente"))
        if not num:
            continue
        tese = _limpa(r.get("tesefirmada"))
        questao = _limpa(r.get("questaosubmetidaajulgamento"))
        situacao = _limpa(r.get("situacao"))
        materia, assuntos = parse_assuntos(r.get("assuntos"))
        ramos_vistos.add(materia)
        data_j = _limpa(r.get("datajulgamento"))
        orgao = _limpa(r.get("orgaojulgador"))
        sumula = _limpa(r.get("sumulaoriginada"))
        rg = re.sub(r"\D", "", _limpa(r.get("numerorepercussaogeralstf")))
        rotulo = {"REP": "Tema", "IAC": "IAC", "PUIL": "PUIL", "SIRDR": "SIRDR"}[esp]
        titulo = questao[:180] + ("…" if len(questao) > 180 else "") if questao else f"{rotulo} {num}/STJ"
        itens.append({
            "id": f"stj-{esp.lower()}-{num}",
            "tribunal": "STJ", "especie": esp,
            "area": materia, "obrigatorio": obrig,
            "validade": _validade(situacao, tese),
            "situacao": " · ".join(x for x in [situacao or NAO_LOCALIZADO,
                        f"julgado em {data_j}" if data_j else "",
                        f"órgão: {orgao}" if orgao else ""] if x),
            "assuntos": assuntos or ["Precedentes do STJ"],
            "numero": f"{rotulo} {num}/STJ",
            "fonte": "STJ — Dados Abertos (Precedentes Qualificados)",
            "titulo": titulo,
            "resumo": (tese or questao or NAO_LOCALIZADO)[:400],
            "completo": tese or NAO_LOCALIZADO,
            "precedentes": (f"Súmula originada: {sumula}" if sumula else ""),
            "vinculos": ([f"stf-tema-{rg}"] if rg else []),
        })
    log(f"STJ: {len(itens)} precedentes qualificados coletados, "
        f"em {len(ramos_vistos)} matérias distintas.")
    return itens
