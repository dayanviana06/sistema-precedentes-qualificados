# -*- coding: utf-8 -*-
"""STF — Camada 2: novidades e verificações por busca na web via API da
Anthropic (o portal do STF bloqueia raspagem; a busca usa o índice público).
Disciplina de zero invenção, imposta no prompt e revalidada no código:
tese VERBATIM + URL da fonte consultada, ou NAO_LOCALIZADO."""
import json, os, re
from util import log, carregar_json
from fontes import NAO_LOCALIZADO

MODELO = "claude-sonnet-4-6"
FERRAMENTAS = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 6}]

PROMPT_NOVIDADES = (
 "Pesquise na web: quais temas de REPERCUSSÃO GERAL do STF tiveram TESE FIXADA, "
 "REAFIRMADA ou ALTERADA nos últimos {dias} dias? Considere apenas fontes oficiais "
 "(stf.jus.br, noticias.stf.jus.br) ou de alta confiabilidade que citem o número do tema. "
 "Para cada um, retorne a TESE VERBATIM (texto integral, sem parafrasear) e a URL da fonte. "
 "REGRAS ABSOLUTAS: não invente números, teses ou datas; se não tiver certeza do texto "
 "integral da tese, use o valor \"NAO_LOCALIZADO\" no campo tese. "
 "Responda APENAS um JSON: {{\"temas\":[{{\"numero\":int,\"titulo\":str,\"tese\":str,"
 "\"situacao\":str,\"fonte_url\":str}}]}}")

PROMPT_TEMA = (
 "Pesquise na web a tese de repercussão geral do TEMA {num} do STF. "
 "Retorne a TESE VERBATIM (texto integral) e a URL da fonte oficial ou de alta "
 "confiabilidade. REGRAS ABSOLUTAS: não parafraseie, não complete, não invente; "
 "qualquer incerteza => tese = \"NAO_LOCALIZADO\". "
 "Responda APENAS um JSON: {{\"numero\":{num},\"titulo\":str,\"tese\":str,"
 "\"situacao\":str,\"fonte_url\":str}}")

def _cliente():
    chave = os.environ.get("ANTHROPIC_API_KEY")
    if not chave:
        raise RuntimeError("ANTHROPIC_API_KEY ausente (camada opcional)")
    import anthropic
    return anthropic.Anthropic(api_key=chave)

def _json_da_resposta(msg):
    txt = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
    ini, fim = txt.find("{"), txt.rfind("}")
    if ini < 0:
        return None
    try:
        return json.loads(txt[ini:fim + 1])
    except Exception:
        return None

def _item(t):
    num = int(re.sub(r"\D", "", str(t.get("numero", ""))) or 0)
    tese = (t.get("tese") or "").strip()
    if not num:
        return None
    if len(tese) < 30 or "NAO_LOCALIZADO" in tese.upper():
        tese = NAO_LOCALIZADO           # curto demais ou incerto: não confiar
    return {
        "id": f"stf-tema-{num}",
        "tribunal": "STF", "especie": "RG",
        "area": "Repercussão Geral — STF", "obrigatorio": True,
        "validade": "Vigente" if tese != NAO_LOCALIZADO else "Pendente — verificar",
        "situacao": (t.get("situacao") or "Tese localizada por busca verificada")
                    + (f" · fonte: {t.get('fonte_url')}" if t.get("fonte_url") else ""),
        "assuntos": ["Repercussão Geral"],
        "numero": f"Tema {num}",
        "fonte": "STF — verificação por busca na web (API Anthropic + web_search)",
        "titulo": (t.get("titulo") or f"Tema {num} da Repercussão Geral")[:180],
        "resumo": tese[:400], "completo": tese,
        "precedentes": "", "vinculos": [],
        "verificado_via": "busca-ia",
    }

def novidades(dias=8, revalidar_pendentes=5):
    cli = _cliente()
    itens = []
    r = cli.messages.create(model=MODELO, max_tokens=2500, tools=FERRAMENTAS,
        messages=[{"role": "user", "content": PROMPT_NOVIDADES.format(dias=dias)}])
    j = _json_da_resposta(r) or {}
    for t in j.get("temas", []):
        it = _item(t)
        if it:
            itens.append(it)
    # revalida alguns temas que ficaram pendentes na base anterior
    base = carregar_json("dados.json", {"itens": []}) or {"itens": []}
    pendentes = [i for i in base["itens"]
                 if i.get("tribunal") == "STF" and i.get("completo") == NAO_LOCALIZADO]
    for p in pendentes[:revalidar_pendentes]:
        num = re.sub(r"\D", "", p["id"])
        r2 = cli.messages.create(model=MODELO, max_tokens=1500, tools=FERRAMENTAS,
            messages=[{"role": "user", "content": PROMPT_TEMA.format(num=num)}])
        j2 = _json_da_resposta(r2)
        it = _item(j2) if j2 else None
        if it and it["completo"] != NAO_LOCALIZADO:
            itens.append(it)
    log(f"STF (busca verificada): {len(itens)} itens obtidos "
        f"({sum(1 for i in itens if i['completo']!=NAO_LOCALIZADO)} com tese verbatim).")
    return itens
