"""Gera analise/comparacao_alternativas.md e analise/resultados.csv a partir dos mesmos
calculos usados pelo assistente (assim o relatorio nunca fica diferente do programa).

Uso:  python analise/gerar_relatorio.py
"""
import csv
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from energia import calculos as c                      # noqa: E402
from energia.dados import carregar_casa, carregar_premissas  # noqa: E402
from energia.respostas import num, reais               # noqa: E402

P, meta = carregar_premissas()
casa = carregar_casa()
itens, total = c.consumo_casa(casa)
medidas, econ, invest = c.pacote_eficiencia(P)
cen = c.comparar(total, econ, invest, P)
base, efic, solar, combo = cen
H = base["horizonte"]
L = []
w = L.append

w("# Análise de consumo e comparação das alternativas\n")
w("> Arquivo gerado por `analise/gerar_relatorio.py`. Todos os números saem de `dados/premissas.json` "
  "e `dados/casa_referencia.csv`. Valores marcados como **estimado** são premissas do grupo, não medições.\n")
w("## 1. Necessidade analisada\n")
w("Abastecer com eletricidade, durante %d anos (%d a %d), uma casa de 4 pessoas na área da Enel SP, "
  "gastando menos e com menor impacto ambiental. As quatro alternativas atendem **a mesma casa no mesmo período**.\n"
  % (H, P["ano_inicio"], P["ano_inicio"] + H - 1))
w("## 2. Análise de consumo (casa de referência — dados estimados)\n")
w("Fórmula: `kWh/mês = potência (W) ÷ 1000 × horas por dia × dias por mês × quantidade`\n")
w("| Equipamento | Qtd | Potência (W) | h/dia | dias/mês | kWh/mês | % |")
w("|---|---:|---:|---:|---:|---:|---:|")
mapa = dict(itens)
for e in sorted(casa, key=lambda x: -mapa[x["equipamento"]]):
    k = mapa[e["equipamento"]]
    f = lambda v, n=2: "—" if v is None else f"{round(v, n):g}".replace(".", ",")
    w(f"| {e['equipamento']} | {e['quantidade']} | {f(e['potencia_w'], 0)} | {f(e['horas_dia'])} | "
      f"{f(e['dias_mes'], 0)} | {num(k)} | {num(k / total * 100)} |")
w(f"| **Total** | | | | | **{num(total)}** | 100 |\n")
w(f"Comparação com dado real: o consumo residencial médio no Brasil foi de {num(P['consumo_medio_residencial_br'])} kWh/mês "
  f"em agosto/2026 (EPE). A casa de referência fica acima da média porque tem 4 moradores e chuveiro elétrico.\n")
t18, t12 = c.tarifa_final(total, P), c.tarifa_final(200, P)
w("### Conta de luz\n")
w(f"- Tarifa sem tributos (ANEEL, REH 3.596/2026): {num(P['tarifa_tusd'], 5)} + {num(P['tarifa_te'], 5)} = "
  f"**R$ {num(P['tarifa_tusd'] + P['tarifa_te'], 5)}/kWh**")
w(f"- Com tributos: `tarifa ÷ (1 − PIS/COFINS) ÷ (1 − ICMS)` → acima de 200 kWh (ICMS 18%): **R$ {num(t18, 4)}/kWh**; "
  f"de 91 a 200 kWh (ICMS 12%): **R$ {num(t12, 4)}/kWh**")
w(f"- Conta atual: {num(total)} kWh × R$ {num(t18, 4)} = **{reais(base['conta_mes_ano1'])} por mês**\n")
w("## 3. Alternativa 1 — Eficiência energética (hábitos + LED)\n")
w("| Medida | Economia (kWh/mês) | Custo |")
w("|---|---:|---:|")
for n_, k, cu in medidas:
    w(f"| {n_} | {num(k)} | {reais(cu)} |")
w(f"| **Total** | **{num(econ)}** | **{reais(invest)}** |\n")
w(f"Novo consumo: {num(total)} − {num(econ)} = **{num(total - econ)} kWh/mês**. Como fica abaixo de 200 kWh, o ICMS cai de 18% "
  f"para 12%: {num(total - econ)} × R$ {num(c.tarifa_final(total - econ, P), 4)} = **{reais(efic['conta_mes_ano1'])} por mês**.\n")
so_kwh = econ * t18
w(f"Atenção: da economia de {reais(efic['economia_mes_ano1'])}/mês, cerca de {reais(so_kwh)} vêm dos kWh economizados e o "
  f"restante da mudança de faixa do ICMS. Numa casa que já consome menos de 200 kWh (ou muito mais), esse segundo ganho não existe.\n")
eg = 55 - P["consumo_geladeira_nova"]
w(f"Medida opcional analisada à parte — geladeira nova eficiente (55 → {num(P['consumo_geladeira_nova'])} kWh/mês): economiza "
  f"{num(eg)} kWh/mês (≈ {reais(eg * t18)}), custa cerca de {reais(P['custo_geladeira_nova'])} e levaria ≈ "
  f"{num(P['custo_geladeira_nova'] / (eg * 12 * t18), 0)} anos para se pagar. Não entra no pacote: só compensa quando a antiga precisa ser trocada.\n")
w("## 4. Alternativa 2 — Energia solar fotovoltaica (fonte renovável)\n")
fv = solar["fv"]
g = c.geracao_por_kwp(P)
d = c.conta_com_fv(total, fv["geracao_kwh"], P["ano_inicio"], P)
w(f"- Geração por kWp: {num(P['irradiacao_hsp'])} kWh/m²·dia × 365 ÷ 12 × {num(P['taxa_desempenho'], 2)} = **{num(g)} kWh/kWp·mês**")
w(f"- Energia a compensar: {num(total)} − {P['disponibilidade_kwh']['bifasica']} (mínimo faturado, ligação bifásica) = "
  f"{num(total - P['disponibilidade_kwh']['bifasica'])} kWh → {fv['modulos']} módulos de {P['modulo_wp']} Wp = "
  f"**{num(fv['kwp'], 2)} kWp**, gerando **{num(fv['geracao_kwh'])} kWh/mês** (≈ {num(fv['area_m2'], 0)} m² de telhado)")
w(f"- Investimento: {num(fv['kwp'] * 1000, 0)} Wp × R$ {num(c.preco_por_wp(fv['kwp'], P), 2)}/Wp = **{reais(fv['investimento'])}**")
w(f"- Conta no 1º ano ({P['ano_inicio']}): consumida na hora {num(d['autoconsumo'])} kWh; injetada {num(d['injetado'])} kWh; "
  f"retirada da rede {num(d['rede'])} kWh; compensada {num(d['compensado'])} kWh; faturada {num(d['faturado'])} kWh")
w(f"- Valor: {num(d['faturado'])} × R$ {num(c.tarifa_final(d['rede'], P), 4)} + {num(d['compensado'])} × R$ {num(P['fio_b'], 2)} × "
  f"{num(c.percentual_fio_b(P['ano_inicio'], P) * 100, 0)}% (Fio B) = **{reais(d['valor'])} por mês**\n")
w("## 5. Alternativa 3 — Eficiência + solar\n")
fv3 = combo["fv"]
w(f"Primeiro reduz o consumo para {num(total - econ)} kWh/mês e só depois dimensiona o sistema: {fv3['modulos']} módulos "
  f"({num(fv3['kwp'], 2)} kWp), {reais(fv3['investimento'])} + {reais(invest)} das medidas = **{reais(combo['investimento'])}**. "
  f"Conta no 1º ano: **{reais(combo['conta_mes_ano1'])} por mês**. Sistemas abaixo de 2 kWp são pouco comuns no mercado e "
  f"tendem a custar mais por Wp que a referência usada; por isso este valor deve ser confirmado com orçamentos.\n")
w(f"## 6. Comparação ({H} anos, valores de hoje, sem inflação nem juros)\n")
w(f"| Alternativa | Renovável | Conta/mês (1º ano) | Investimento | Retorno | Custo total em {H} anos | Economia líquida | CO₂ evitado/ano |")
w("|---|:-:|---:|---:|---:|---:|---:|---:|")
linhas_csv = [["alternativa", "renovavel", "consumo_rede_kwh_mes", "geracao_kwh_mes", "conta_mes_ano1_R$", "investimento_R$",
               "payback_anos", f"custo_total_{H}anos_R$", "economia_liquida_R$", "co2_evitado_kg_ano"]]
for x in cen:
    pb = x["payback_anos"]
    pbt = "—" if x["investimento"] == 0 else ("não se paga" if pb is None else (("1 mês" if round(pb * 12) <= 1 else f"{round(pb * 12)} meses") if pb < 2 else f"{num(pb)} anos"))
    w(f"| {x['nome']} | {'sim' if x['renovavel'] else 'não'} | {reais(x['conta_mes_ano1'])} | {reais(x['investimento'])} | {pbt} | "
      f"{reais(x['custo_total'])} | {reais(x['economia_total'])} | {num(x['co2_kg_ano'], 0)} kg |")
    linhas_csv.append([x["nome"], x["renovavel"], round(x["consumo_kwh"], 1), round(x["geracao_kwh"], 1),
                       round(x["conta_mes_ano1"], 2), round(x["investimento"], 2),
                       "" if pb is None else round(pb, 2), round(x["custo_total"], 2),
                       round(x["economia_total"], 2), round(x["co2_kg_ano"], 1)])
w("")
w(f"CO₂ evitado = kWh que deixam de vir da rede × {num(P['fator_emissao_sin'], 4)} tCO₂/MWh (fator médio do SIN em 2025, MCTI). "
  "Como a rede brasileira já é majoritariamente renovável, o valor em kg é pequeno; não inclui as emissões de fabricação dos módulos.\n")
w("## 7. Análise de sensibilidade do cenário solar (premissas estimadas)\n")
for chave, vals, rot, casas in [("fio_b", [0.10, 0.15, 0.20, 0.25], "Fio B (R$/kWh)", 2),
                                ("simultaneidade", [0.15, 0.30, 0.45], "Simultaneidade", 2),
                                ("irradiacao_hsp", [4.2, 4.5, 4.8], "Irradiação (kWh/m²·dia)", 1)]:
    w(f"| {rot} | Conta/mês (1º ano) | Retorno (anos) | Economia líquida em {H} anos |")
    w("|---:|---:|---:|---:|")
    for v, conta, pb, ec in c.sensibilidade(total, econ, invest, P, chave, vals):
        w(f"| {num(v, casas)} | {reais(conta)} | {'—' if pb is None else num(pb)} | {reais(ec)} |")
    w("")
w("Leitura: mesmo no pior caso testado o sistema se paga dentro do período, mas o retorno muda — por isso o assistente "
  "apresenta os números como estimativa e orienta a pedir simulação com a conta real.\n")

(RAIZ / "analise" / "comparacao_alternativas.md").write_text("\n".join(L), encoding="utf-8")
with open(RAIZ / "analise" / "resultados.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(linhas_csv)
print("Gerados: analise/comparacao_alternativas.md e analise/resultados.csv")
