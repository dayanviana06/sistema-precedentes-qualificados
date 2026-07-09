# -*- coding: utf-8 -*-
import hashlib, json, re, sys, time, unicodedata
import requests

UA = {
    # O WAF do portal do STJ (dadosabertos.web.stj.jus.br) devolve 403 Forbidden
    # para User-Agents que se identificam como robô/coletor. Usamos um
    # cabeçalho de navegador comum — o conteúdo baixado continua sendo, em
    # tudo o mais, o mesmo arquivo público de dados abertos; não há raspagem
    # de página nem burla de autenticação, apenas o download do CSV oficial.
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
    "Accept": "text/csv,application/csv,text/plain,*/*",
    "Accept-Language": "pt-BR,pt;q=0.9",
}

def baixar(url, tentativas=3, timeout=60, binario=False):
    """Download com tentativas. Lança exceção após esgotar — o consolidador
    trata a falha preservando os dados anteriores (nunca inventa)."""
    ultimo = None
    for i in range(tentativas):
        try:
            r = requests.get(url, headers=UA, timeout=timeout)
            r.raise_for_status()
            if binario:
                return r.content
            # Decodifica de forma robusta: as fontes oficiais (STJ/STF) são
            # UTF-8, mas nem sempre enviam o charset no cabeçalho, o que fazia
            # a biblioteca supor Latin-1 e desconfigurar os acentos. Tentamos
            # UTF-8 primeiro e só então codificações legadas.
            bruto = r.content
            for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
                try:
                    return bruto.decode(enc)
                except UnicodeDecodeError:
                    continue
            return bruto.decode("utf-8", errors="replace")
        except Exception as e:
            ultimo = e
            time.sleep(3 * (i + 1))
    raise RuntimeError(f"Falha ao baixar {url}: {ultimo}")

def slug(s):
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def sha(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:16]

def log(msg):
    print(f"[coletor] {msg}", file=sys.stderr)

def carregar_json(caminho, padrao=None):
    try:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return padrao

def salvar_json(caminho, obj):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
