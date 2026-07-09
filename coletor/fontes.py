# -*- coding: utf-8 -*-
"""Endereços oficiais das fontes. Verificados em julho/2026.
Se algum endereço mudar, ajuste apenas aqui."""

STJ_TEMAS_CSV = ("https://dadosabertos.web.stj.jus.br/dataset/"
    "4238da2f-c07b-4c1a-b345-4402accacdcf/resource/"
    "df29da13-7d6b-41ba-ad96-cd1a5bbd191c/download/temas.csv")
STJ_PROCESSOS_CSV = ("https://dadosabertos.web.stj.jus.br/dataset/"
    "4238da2f-c07b-4c1a-b345-4402accacdcf/resource/"
    "7ed21202-0049-4fcb-aa7c-48d810d3c499/download/processos.csv")

# STF: o portal (portal.stf.jus.br) e o site de noticias BLOQUEIAM robôs.
# Por isso o coletor do STF NÃO raspa páginas: usa (1) o CSV oficial do
# Painel de Repercussão Geral do Corte Aberta (exportação manual ocasional,
# arquivo local 'stf-temas.csv') e (2) busca na web verificada via API da
# Anthropic (verificador_stf.py) para novidades diárias e revalidações.
STF_CORTE_ABERTA_PAINEL = "https://transparencia.stf.jus.br/extensions/repercussao_geral/repercussao_geral.html"

# Fichas oficiais do NUGEPNAC/TJMA (PDFs). Acrescente novas fichas a esta lista.
TJMA_FICHAS_PDF = [
  "https://novogerenciador.tjma.jus.br/storage/arquivos/site_nugepnac/irdr_tema_04_17_06_2022_19_46_06.pdf",
  "https://novogerenciador.tjma.jus.br/storage/arquivos/site_nugepnac/irdr_tema_05_24_06_2022_18_54_20.pdf",
]
TJMA_HOTSITE_IRDR = "https://www.tjma.jus.br/hotsite/nugepnac/item/1992/0/irdr-admitido"

NAO_LOCALIZADO = "NAO_LOCALIZADO"

# STJ — Espelhos de Acórdãos (Dados Abertos, CSV, CC-BY). Opcional: cole aqui
# as URLs "download" dos recursos desejados (Corte Especial, Seções, Turmas),
# obtidas em https://dadosabertos.web.stj.jus.br/dataset/ .
STJ_ESPELHOS_CSV = []
