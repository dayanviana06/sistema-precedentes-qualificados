# -*- coding: utf-8 -*-
"""Orquestrador diário. Cada fonte falha de forma independente:
se uma cair, as outras seguem e a base anterior daquela fonte é preservada."""
from util import log
import consolidar, enriquecer

def _seguro(nome, fn):
    try:
        return fn()
    except Exception as e:
        log(f"{nome}: coleta indisponível hoje ({e}) — base anterior preservada.")
        return []

def main():
    import coletor_stj, coletor_stf, coletor_tjma, coletor_informativos
    coletas = [
        _seguro("STJ", coletor_stj.coletar),
        _seguro("STF", coletor_stf.coletar),
        _seguro("TJMA", coletor_tjma.coletar),
        _seguro("Informativos", coletor_informativos.coletar),
    ]
    consolidar.consolidar(coletas)
    enriquecer.enriquecer()
    log("Atualização concluída.")

if __name__ == "__main__":
    main()
