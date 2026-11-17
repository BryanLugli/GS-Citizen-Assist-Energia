"""Leitura das premissas (dados/premissas.json) e da casa de referencia."""
import csv
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQ_PREMISSAS = RAIZ / "dados" / "premissas.json"
ARQ_CASA = RAIZ / "dados" / "casa_referencia.csv"


def carregar_premissas(caminho=ARQ_PREMISSAS):
    """Devolve (valores, metadados). valores[chave] = numero; metadados[chave] = fonte, tipo..."""
    with open(caminho, encoding="utf-8") as f:
        bruto = json.load(f)
    meta = {k: v for k, v in bruto.items() if not k.startswith("_")}
    valores = {k: v["valor"] for k, v in meta.items()}
    return valores, meta


def carregar_casa(caminho=ARQ_CASA):
    """Lista de equipamentos da casa de referencia."""
    casa = []
    with open(caminho, encoding="utf-8", newline="") as f:
        for lin in csv.DictReader(f):
            num = lambda c: float(lin[c]) if lin[c] not in ("", None) else None
            casa.append({
                "equipamento": lin["equipamento"],
                "quantidade": int(lin["quantidade"]),
                "potencia_w": num("potencia_w"),
                "horas_dia": num("horas_dia"),
                "dias_mes": num("dias_mes"),
                "kwh_mes_fixo": num("kwh_mes_fixo"),
                "tipo_dado": lin["tipo_dado"],
                "observacao": lin["observacao"],
            })
    return casa
