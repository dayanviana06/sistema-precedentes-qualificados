# -*- coding: utf-8 -*-
"""Consolida coletas com a base anterior, sob regra de zero invenção:
1. NAO_LOCALIZADO nunca sobrescreve valor anterior válido.
2. A camada didática (emSuma, explicacao, mnemonico, fluxograma,
   dispositivos, vinculos, assuntos, area) é preservada da base anterior.
3. Toda tese ou situação alterada entra no changelog do dia.
4. dados-manual.json (curadoria do magistrado) tem prioridade máxima."""
from datetime import date
from fontes import NAO_LOCALIZADO
from util import carregar_json, salvar_json, log, sha

DIDATICOS = ("emSuma", "explicacao", "mnemonico", "fluxograma",
             "dispositivos", "vinculos", "assuntos", "area")
OFICIAIS = ("completo", "resumo", "situacao", "validade",
            "fonte", "titulo", "precedentes")

def _mesclar(anterior: dict, novo: dict) -> dict:
    saida = dict(anterior)
    for k in OFICIAIS:
        v = novo.get(k)
        if v and v != NAO_LOCALIZADO:
            saida[k] = v
    for k in DIDATICOS:
        if anterior.get(k):
            saida[k] = anterior[k]
        elif novo.get(k):
            saida[k] = novo[k]
    return saida

def consolidar(coletas, caminho_anterior="dados.json",
               caminho_manual="dados-manual.json",
               caminho_saida="dados.json",
               caminho_changelog="changelog.json"):
    base = carregar_json(caminho_anterior, {"itens": []}) or {"itens": []}
    manual = carregar_json(caminho_manual, {"itens": []}) or {"itens": []}
    por_id = {i["id"]: i for i in base.get("itens", []) if i.get("id")}
    novos, alterados = [], []

    for itens in coletas:
        for novo in itens or []:
            if not novo.get("id"):
                continue
            ant = por_id.get(novo["id"])
            if ant is None:
                por_id[novo["id"]] = novo
                if novo.get("completo") and novo["completo"] != NAO_LOCALIZADO:
                    novos.append({"id": novo["id"], "numero": novo.get("numero"),
                                  "titulo": novo.get("titulo")})
            else:
                antes = sha((ant.get("completo") or "") + (ant.get("situacao") or ""))
                mesclado = _mesclar(ant, novo)
                depois = sha((mesclado.get("completo") or "") + (mesclado.get("situacao") or ""))
                por_id[novo["id"]] = mesclado
                if antes != depois:
                    alterados.append({"id": novo["id"], "numero": mesclado.get("numero"),
                                      "situacao": mesclado.get("situacao")})

    for it in manual.get("itens", []):
        if it.get("id"):
            por_id[it["id"]] = {**por_id.get(it["id"], {}), **it}

    itens_final = sorted(por_id.values(),
                         key=lambda d: (d.get("tribunal", ""), d.get("area", ""), d.get("numero", "")))
    hoje = date.today().isoformat()
    salvar_json(caminho_saida, {
        "versao": 1, "gerado_em": hoje,
        "fontes": ["STF (Repercussão Geral)",
                   "STJ (Dados Abertos — Precedentes Qualificados)",
                   "TJMA (NUGEPNAC — fichas de IRDR/IAC)"],
        "itens": itens_final})
    salvar_json(caminho_changelog, {"data": hoje, "novos": novos, "alterados": alterados})
    log(f"Consolidado: {len(itens_final)} itens · {len(novos)} novos · {len(alterados)} alterados.")
    return len(novos), len(alterados)
