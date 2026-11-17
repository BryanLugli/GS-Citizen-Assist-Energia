"""Calculos de consumo, conta de luz, eficiencia e energia solar fotovoltaica.

Formulas principais
-------------------
Energia (kWh) = Potencia (W) / 1000 x tempo de uso (h)
Tarifa com tributos = (TUSD + TE) / (1 - PIS/COFINS) / (1 - ICMS)      [tributos "por dentro"]
Geracao FV (kWh/mes) = kWp x HSP x (365/12) x taxa de desempenho
CO2 evitado (kg) = energia que deixou de vir da rede (kWh) x fator de emissao do SIN (kg/kWh)

Todas as funcoes recebem o dicionario P (premissas) para que nenhum numero fique escondido.
"""
import math


# ---------------------------------------------------------------- consumo
def kwh_equipamento(potencia_w, horas_dia, dias_mes=30, quantidade=1):
    """Energia mensal de um equipamento, em kWh."""
    if potencia_w < 0 or horas_dia < 0 or dias_mes < 0 or quantidade < 0:
        raise ValueError("valores negativos nao sao validos")
    if horas_dia > 24 or dias_mes > 31:
        raise ValueError("horas_dia deve ser <= 24 e dias_mes <= 31")
    return potencia_w / 1000 * horas_dia * dias_mes * quantidade


def consumo_casa(casa):
    """Devolve lista [(equipamento, kWh/mes)] ordenada do maior para o menor, e o total."""
    itens = []
    for e in casa:
        if e["kwh_mes_fixo"] is not None:
            kwh = e["kwh_mes_fixo"] * e["quantidade"]
        else:
            kwh = kwh_equipamento(e["potencia_w"], e["horas_dia"], e["dias_mes"], e["quantidade"])
        itens.append((e["equipamento"], kwh))
    itens.sort(key=lambda x: -x[1])
    return itens, sum(k for _, k in itens)


# ---------------------------------------------------------------- conta de luz
def aliquota_icms(kwh, P):
    for limite, aliq in P["icms_faixas"]:
        if limite is None or kwh <= limite:
            return aliq
    return P["icms_faixas"][-1][1]


def tarifa_final(kwh_referencia, P):
    """R$/kWh com PIS/COFINS e ICMS. A faixa de ICMS depende do consumo do mes."""
    base = P["tarifa_tusd"] + P["tarifa_te"]
    return base / (1 - P["pis_cofins"]) / (1 - aliquota_icms(kwh_referencia, P))


def conta_mensal(kwh, P, ligacao="bifasica"):
    """Valor da conta sem geracao propria (bandeira verde, sem taxa de iluminacao publica)."""
    if kwh < 0:
        raise ValueError("consumo negativo")
    minimo = P["disponibilidade_kwh"][ligacao]
    faturado = max(kwh, minimo)
    return faturado * tarifa_final(kwh, P)


# ---------------------------------------------------------------- eficiencia
def economia_banho(pessoas, min_atual, min_novo, potencia_w=5500, dias=30):
    """kWh/mes economizados ao reduzir o tempo de banho."""
    if min_novo > min_atual:
        raise ValueError("o novo tempo deve ser menor ou igual ao atual")
    return kwh_equipamento(potencia_w, pessoas * (min_atual - min_novo) / 60, dias)


def economia_led(n_lampadas, w_atual=20, w_led=9, horas_dia=5, dias=30):
    """kWh/mes economizados ao trocar lampadas por LED de mesmo fluxo luminoso."""
    return kwh_equipamento(max(w_atual - w_led, 0), horas_dia, dias, n_lampadas)


def economia_standby(w_standby=10, fracao_cortada=0.7, dias=30):
    return kwh_equipamento(w_standby * fracao_cortada, 24, dias)


def pacote_eficiencia(P, pessoas=4, min_atual=8, min_novo=6, potencia_chuveiro=5500,
                      n_lampadas=8, w_lampada=20, cortar_standby=True):
    """Pacote de baixo custo: banho mais curto + LED + corte de stand-by."""
    medidas = []
    e = economia_banho(pessoas, min_atual, min_novo, potencia_chuveiro)
    medidas.append((f"Banho de {min_atual:g} para {min_novo:g} min ({pessoas} pessoas)", e, 0.0))
    e = economia_led(n_lampadas, w_lampada)
    medidas.append((f"Trocar {n_lampadas} lampadas de {w_lampada:g} W por LED 9 W", e,
                    n_lampadas * P["custo_lampada_led"]))
    if cortar_standby:
        medidas.append(("Regua com interruptor para cortar 70% do stand-by",
                        economia_standby(), P["custo_regua"]))
    return medidas, sum(m[1] for m in medidas), sum(m[2] for m in medidas)


# ---------------------------------------------------------------- solar fotovoltaica
def geracao_por_kwp(P):
    """kWh por mes gerados por 1 kWp instalado (media anual)."""
    return P["irradiacao_hsp"] * 365 / 12 * P["taxa_desempenho"]


def preco_por_wp(kwp, P):
    """Interpola o preco entre os sistemas de 2 kWp e 4 kWp do estudo da Greener."""
    p2, p4 = P["preco_fv_2kwp"], P["preco_fv_4kwp"]
    if kwp <= 2:
        return p2
    if kwp >= 4:
        return p4
    return p2 + (p4 - p2) * (kwp - 2) / 2


def dimensionar_fv(consumo_kwh, P, ligacao="bifasica"):
    """Sistema que cobre o consumo acima do minimo faturado (gerar mais que isso nao reduz a conta)."""
    alvo = max(consumo_kwh - P["disponibilidade_kwh"][ligacao], 0)
    kwp_mod = P["modulo_wp"] / 1000
    n = max(1, round(alvo / geracao_por_kwp(P) / kwp_mod))
    kwp = n * kwp_mod
    return {"modulos": n, "kwp": kwp, "geracao_kwh": kwp * geracao_por_kwp(P),
            "investimento": kwp * 1000 * preco_por_wp(kwp, P),
            "area_m2": n * 2.6}


def percentual_fio_b(ano, P):
    tab = P["fio_b_percentual"]
    return tab.get(str(ano), tab["2029+"] if ano >= 2029 else tab["2026"])


def conta_com_fv(consumo_kwh, geracao_kwh, ano, P, ligacao="bifasica"):
    """Conta mensal com geracao propria nas regras da Lei 14.300 (sistema novo, GD II).

    Simplificacoes (ver docs/justificativas.md): media anual sem sazonalidade; faixa de ICMS
    definida pela energia retirada da rede; Fio B cobrado sem tributos.
    """
    minimo = P["disponibilidade_kwh"][ligacao]
    auto = min(geracao_kwh * P["simultaneidade"], consumo_kwh)   # consumida na hora
    injetado = geracao_kwh - auto                                # vai para a rede e vira credito
    rede = consumo_kwh - auto                                    # retirado da rede
    compensado = min(injetado, max(rede - minimo, 0))
    faturado = max(rede - compensado, minimo)
    valor = faturado * tarifa_final(rede, P) + compensado * P["fio_b"] * percentual_fio_b(ano, P)
    return {"valor": valor, "autoconsumo": auto, "injetado": injetado, "rede": rede,
            "compensado": compensado, "faturado": faturado, "credito_sobra": injetado - compensado}


# ---------------------------------------------------------------- comparacao
def _payback_anos(investimento, economias_anuais):
    """Ano (com fracao) em que a economia acumulada paga o investimento; None se nao paga."""
    if investimento <= 0:
        return 0.0
    acum = 0.0
    for i, e in enumerate(economias_anuais):
        if e > 0 and acum + e >= investimento:
            return i + (investimento - acum) / e
        acum += e
    return None


def comparar(consumo_kwh, econ_efic_kwh, invest_efic, P, ligacao="bifasica", horizonte=None):
    """Compara 4 cenarios para a MESMA necessidade (abastecer a mesma casa) no MESMO periodo.

    0 - Situacao atual | 1 - Eficiencia | 2 - Solar fotovoltaica | 3 - Eficiencia + solar
    """
    H = horizonte or P["horizonte_anos"]
    ano0 = P["ano_inicio"]
    fe = P["fator_emissao_sin"]  # tCO2/MWh = kgCO2/kWh
    econ_efic_kwh = min(econ_efic_kwh, consumo_kwh)
    conta_base = conta_mensal(consumo_kwh, P, ligacao)

    def cenario(nome, consumo, invest, fv=None, renovavel=False):
        contas = []
        for i in range(H):
            if fv:
                ger = fv["geracao_kwh"] * (1 - P["degradacao_anual"]) ** i
                c = conta_com_fv(consumo, ger, ano0 + i, P, ligacao)
                contas.append(c["valor"] * 12)
            else:
                contas.append(conta_mensal(consumo, P, ligacao) * 12)
        economias = [conta_base * 12 - c for c in contas]
        evitado_kwh = (consumo_kwh - consumo) + (fv["geracao_kwh"] if fv else 0)
        return {"nome": nome, "renovavel": renovavel, "consumo_kwh": consumo,
                "geracao_kwh": fv["geracao_kwh"] if fv else 0.0, "fv": fv,
                "investimento": invest, "conta_mes_ano1": contas[0] / 12,
                "economia_mes_ano1": economias[0] / 12,
                "payback_anos": _payback_anos(invest, economias),
                "custo_total": invest + sum(contas), "economia_total": sum(economias) - invest,
                "co2_kg_ano": evitado_kwh * 12 * fe, "horizonte": H}

    reduzido = consumo_kwh - econ_efic_kwh
    fv_a = dimensionar_fv(consumo_kwh, P, ligacao)
    fv_b = dimensionar_fv(reduzido, P, ligacao)
    return [
        cenario("Situacao atual", consumo_kwh, 0.0),
        cenario("Eficiencia (habitos + LED)", reduzido, invest_efic),
        cenario("Solar fotovoltaica", consumo_kwh, fv_a["investimento"], fv_a, True),
        cenario("Eficiencia + solar", reduzido, invest_efic + fv_b["investimento"], fv_b, True),
    ]


def recomendar(cenarios, pode_instalar_fv=True):
    """Regra de recomendacao coerente com a analise (ver docs/justificativas.md)."""
    efic, solar, combo = cenarios[1], cenarios[2], cenarios[3]
    passos = ["Comece pela eficiencia: custa pouco, nao depende de obra e reduz a conta ja no 1o mes."]
    if not pode_instalar_fv:
        passos.append("Sem telhado proprio (aluguel/apartamento), a energia solar no local nao e viavel: "
                      "fique com a eficiencia e avalie depois uma assinatura de energia solar compartilhada.")
        return efic, passos
    pb = combo["payback_anos"]
    if pb is not None and pb <= 6 and combo["economia_total"] > efic["economia_total"]:
        passos.append("Depois, se houver telhado proprio sem sombra e dinheiro (ou credito barato), "
                      "instale o sistema solar JA dimensionado para o consumo reduzido: ele fica menor e mais barato.")
        return combo, passos
    passos.append("Neste perfil a energia solar demora para se pagar: fique com a eficiencia e reavalie "
                  "se o consumo ou a tarifa subirem.")
    return efic, passos


def sensibilidade(consumo_kwh, econ_kwh, invest, P, chave, valores, ligacao="bifasica"):
    """Recalcula o cenario solar variando uma premissa estimada."""
    saida = []
    for v in valores:
        Q = dict(P)
        Q[chave] = v
        c = comparar(consumo_kwh, econ_kwh, invest, Q, ligacao)[2]
        saida.append((v, c["conta_mes_ano1"], c["payback_anos"], c["economia_total"]))
    return saida
