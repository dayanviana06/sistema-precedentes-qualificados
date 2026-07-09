# -*- coding: utf-8 -*-
"""Camada didática opcional via API da Anthropic (ANTHROPIC_API_KEY).
Regra inegociável: a IA apenas REFORMULA a tese oficial já coletada;
é proibida de citar norma, número ou precedente que não esteja no texto
de entrada. Campos gerados recebem a marca 'gerado_por_ia'."""
import json, os
from util import carregar_json, salvar_json, log
from fontes import NAO_LOCALIZADO

PROMPT = (
 "Você é assistente de um juiz de direito brasileiro. Abaixo está a TESE OFICIAL "
 "de um precedente. Produza JSON com: emSuma (1 frase, linguagem simples) e "
 "explicacao (2 a 3 frases práticas). REGRAS ABSOLUTAS: use somente o que está "
 "na tese; não cite artigos, números, precedentes ou fatos que não constem dela; "
 "não acrescente nada incerto. Responda apenas o JSON.\n\nTESE OFICIAL:\n{tese}")

def enriquecer(caminho="dados.json", limite=40):
    chave = os.environ.get("ANTHROPIC_API_KEY")
    if not chave:
        log("Enriquecimento: ANTHROPIC_API_KEY ausente — etapa pulada (opcional).")
        return
    import anthropic
    cli = anthropic.Anthropic(api_key=chave)
    dados = carregar_json(caminho)
    feitos = 0
    for it in dados["itens"]:
        if feitos >= limite:
            break
        tese = it.get("completo", "")
        if not tese or tese == NAO_LOCALIZADO or it.get("emSuma"):
            continue
        try:
            r = cli.messages.create(
                model="claude-sonnet-4-6", max_tokens=400,
                messages=[{"role": "user", "content": PROMPT.format(tese=tese[:4000])}])
            txt = r.content[0].text.strip().strip("`")
            txt = txt[txt.find("{"): txt.rfind("}") + 1]
            j = json.loads(txt)
            if j.get("emSuma"):
                it["emSuma"] = j["emSuma"]
                it["explicacao"] = j.get("explicacao", "")
                it["gerado_por_ia"] = True
                feitos += 1
        except Exception as e:
            log(f"Enriquecimento: item {it.get('id')} pulado ({e}).")
    salvar_json(caminho, dados)
    log(f"Enriquecimento: {feitos} itens receberam camada didática (marcados gerado_por_ia).")
