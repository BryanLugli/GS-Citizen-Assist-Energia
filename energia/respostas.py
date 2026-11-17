"""Respostas do assistente. Todo numero vem das premissas ou dos calculos - nada e inventado aqui."""
import unicodedata

from . import calculos as c

AVISO = ("Aviso: este assistente e um prototipo academico (FIAP). Nao e canal oficial da Enel, da ANEEL "
         "ou de qualquer orgao publico. Os valores sao ESTIMATIVAS e nao garantem economia, geracao ou custo. "
         "Nenhum dado pessoal e pedido ou guardado.")

LIMITACOES = [
    "Tarifa da Enel SP (capital e Grande Sao Paulo), bandeira verde, sem taxa de iluminacao publica.",
    "PIS/COFINS muda todo mes; usamos 6%. A faixa de ICMS muda em 90 e 200 kWh: perto desses limites a conta pode variar bastante.",
    "A geracao solar e uma media anual: no inverno gera menos, no verao mais. Sombra, inclinacao e direcao do telhado mudam o resultado.",
    "O valor do Fio B e a regra depois de 2028 sao premissas nossas. Peca ao instalador a simulacao com a sua conta real.",
    "Precos de sistema solar sao medias nacionais (Greener, jun/2026). Peca pelo menos 3 orcamentos.",
    "Nao consideramos juros de financiamento, inflacao da tarifa, troca do inversor nem as emissoes da fabricacao dos paineis.",
]


def _meses(anos):
    m = max(1, round(anos * 12))
    return "1 mes" if m == 1 else f"{m} meses"


def reais(v):
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def num(v, casas=1):
    return f"{v:.{casas}f}".replace(".", ",")


def _norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    return "".join(ch for ch in t if unicodedata.category(ch) != "Mn")


def fontes_usadas(meta, chaves):
    linhas = []
    for k in chaves:
        m = meta[k]
        marca = "REAL" if m["tipo"] == "real" else "ESTIMADO"
        linhas.append(f"  [{marca}] {m['fonte']}" + (f" - {m['url']}" if m["url"] else ""))
    return "\n".join(linhas)


def texto_comparacao(cenarios, P):
    H = cenarios[0]["horizonte"]
    L = [f"{'Alternativa':<28}{'Conta/mes':>12}{'Investimento':>15}{'Retorno':>12}{'Custo em ' + str(H) + ' anos':>20}{'CO2 evitado/ano':>18}"]
    for x in cenarios:
        pb = x["payback_anos"]
        pb_t = "-" if x["investimento"] == 0 else ("nao se paga" if pb is None else
                                                    (_meses(pb) if pb < 2 else f"{num(pb)} anos"))
        nome = x["nome"] + (" *" if x["renovavel"] else "")
        L.append(f"{nome:<28}{reais(x['conta_mes_ano1']):>12}{reais(x['investimento']):>15}{pb_t:>12}"
                 f"{reais(x['custo_total']):>20}{num(x['co2_kg_ano'], 0) + ' kg':>18}")
    L.append("* usa fonte renovavel (solar). Conta/mes = estimativa do 1o ano.")
    return "\n".join(L)


def texto_recomendacao(cenarios, P, pode_fv=True):
    escolhido, passos = c.recomendar(cenarios, pode_fv)
    base = cenarios[0]
    L = ["O QUE RECOMENDAMOS (estimativa, nao e garantia):"]
    L += [f"  {i}. {p}" for i, p in enumerate(passos, 1)]
    L.append(f"  Resultado estimado de '{escolhido['nome']}': conta de {reais(base['conta_mes_ano1'])} para cerca de "
             f"{reais(escolhido['conta_mes_ano1'])} por mes, investindo {reais(escolhido['investimento'])}.")
    fv = escolhido["fv"]
    if fv:
        L.append(f"  Sistema solar estimado: {fv['modulos']} placas ({num(fv['kwp'], 2)} kWp), cerca de "
                 f"{num(fv['area_m2'], 0)} m2 de telhado, gerando em media {num(fv['geracao_kwh'], 0)} kWh/mes.")
        if fv["kwp"] < 2:
            L.append("  Atencao: sistemas menores que 2 kWp sao pouco comuns e costumam custar mais por placa do que "
                     "a media usada aqui. Confirme com orcamentos reais antes de decidir.")
        L.append("  Mesmo com solar a conta nao zera: existe um consumo minimo cobrado e a taxa de uso da rede (Fio B).")
    return "\n".join(L)


# --------------------------------------------------------------- perguntas frequentes
TEMAS = [
    ("Como economizar na conta de luz?", "economizar"),
    ("Quanto gasta o chuveiro / banho?", "chuveiro"),
    ("Vale a pena trocar por lampada LED?", "led"),
    ("Aparelho desligado na tomada gasta?", "stand-by"),
    ("Vale a pena trocar a geladeira?", "geladeira"),
    ("Quanto custa o kWh na Enel SP?", "tarifa"),
    ("Como o imposto (ICMS) muda a conta?", "icms"),
    ("Vale a pena colocar placa solar?", "placa solar"),
    ("Moro de aluguel, posso ter placa solar?", "placa solar aluguel"),
    ("O que e o Fio B / taxacao do sol?", "fio b"),
    ("Qual o impacto no meio ambiente?", "co2"),
]


def texto_temas():
    return "\n".join(f"   {i:>2} - {pergunta}" for i, (pergunta, _) in enumerate(TEMAS, 1))


def responder(pergunta, P, meta):
    """Procura palavras-chave e devolve (resposta, chaves das fontes). Sem IA generativa: resposta rastreavel.
    O usuario tambem pode digitar o numero de um tema da lista TEMAS."""
    bruto = pergunta.strip()
    if bruto.isdigit() and 1 <= int(bruto) <= len(TEMAS):
        pergunta = TEMAS[int(bruto) - 1][1]
    q = _norm(pergunta)
    t = lambda *ps: any(p in q for p in ps)
    tarifa = c.tarifa_final(250, P)
    if t("fio b", "taxa do sol", "taxacao", "taxa da rede", "taxa de uso", "conta nao zera", "nao zera"):
        ano = P["ano_inicio"]
        return (f"Quem instala energia solar hoje paga uma parte da tarifa de uso da rede (o 'Fio B') sobre a energia "
                f"que manda para a rede e depois usa como credito. Pela Lei 14.300 essa parte e de 60% em 2026, 75% em 2027 "
                f"e 90% em 2028. Nas nossas contas usamos Fio B de {reais(P['fio_b'])}/kWh (valor estimado). "
                f"Por isso o credito vale um pouco menos que o kWh comprado e a conta nunca chega a zero.",
                ["fio_b_percentual", "fio_b"])
    if t("solar", "placa", "painel", "paineis", "fotovolt", "gerar energia", "gerar minha", "propria energia", "telhado"):
        if t("apartamento", "aluguel", "alugad", "inquilin", "nao e minha", "nao tenho telhado"):
            return ("Para instalar placas voce precisa de um telhado seu (ou autorizacao do dono/condominio), sem sombra. "
                    "Em aluguel ou apartamento, normalmente o melhor caminho e a eficiencia: banho mais curto, LED e cortar o stand-by.",
                    [])
        g = c.geracao_por_kwp(P)
        return (f"Em Sao Paulo, cada 1 kWp de placas gera em media cerca de {num(g, 0)} kWh por mes (estimativa). "
                f"Um sistema pequeno (2 kWp) custa perto de {reais(P['preco_fv_2kwp'] * 2000)} instalado e um de 4 kWp perto de "
                f"{reais(P['preco_fv_4kwp'] * 4000)} (media nacional, jun/2026). Vale mais a pena para quem tem telhado proprio "
                f"sem sombra e conta acima de uns 200 kWh. Use a opcao 2 do menu para simular com a sua conta.",
                ["irradiacao_hsp", "taxa_desempenho", "preco_fv_2kwp", "preco_fv_4kwp"])
    if t("chuveiro", "banho", "mais gasta", "gasta mais", "maior gasto", "vilao", "agua quente"):
        e = c.economia_banho(1, 8, 6)
        return (f"O chuveiro eletrico costuma ser o maior gasto da casa. Um chuveiro de 5.500 W gasta cerca de 0,09 kWh por minuto. "
                f"Cada pessoa que reduz o banho de 8 para 6 minutos economiza cerca de {num(e)} kWh por mes "
                f"(perto de {reais(e * tarifa)}). No calor, use a chave na posicao 'verao'.",
                ["tarifa_tusd", "tarifa_te"])
    if t("led", "lampada", "luz acesa", "luzes", "iluminacao", "bocal"):
        e = c.economia_led(1)
        return (f"Trocar uma lampada fluorescente de 20 W por uma LED de 9 W (mesma claridade), acesa 5 h por dia, economiza "
                f"cerca de {num(e, 2)} kWh por mes ({reais(e * tarifa)}). A lampada custa perto de {reais(P['custo_lampada_led'])} "
                f"e se paga em cerca de {num(P['custo_lampada_led'] / (e * tarifa), 0)} meses. Comece pelas que ficam mais tempo acesas.",
                ["custo_lampada_led", "tarifa_tusd"])
    if t("stand", "tomada", "desligad", "luzinha", "carregador", "tirar da tomada"):
        e = c.economia_standby()
        return (f"Aparelhos 'desligados' na tomada continuam gastando. Cortar 70% de um stand-by de 10 W economiza cerca de "
                f"{num(e)} kWh por mes ({reais(e * tarifa)}). Uma regua com interruptor resolve.",
                ["custo_regua"])
    if t("geladeira", "freezer", "refrigerador", "eletrodomestico novo", "trocar aparelho"):
        e = 55 - P["consumo_geladeira_nova"]
        anos = P["custo_geladeira_nova"] / (e * 12 * tarifa)
        return (f"Trocar uma geladeira antiga (cerca de 55 kWh/mes, estimativa) por uma nova eficiente "
                f"({num(P['consumo_geladeira_nova'])} kWh/mes, etiqueta) economiza cerca de {num(e, 0)} kWh por mes "
                f"({reais(e * tarifa)}), mas a geladeira custa perto de {reais(P['custo_geladeira_nova'])}: so pela economia "
                f"levaria cerca de {num(anos, 0)} anos para se pagar. Vale a pena quando a antiga ja precisa ser trocada. "
                f"Enquanto isso: borracha da porta em bom estado, longe do fogao e sem roupa secando atras.",
                ["custo_geladeira_nova", "consumo_geladeira_nova"])
    if t("icms", "imposto", "200", "faixa", "tributo"):
        return (f"Em Sao Paulo o ICMS da conta residencial depende do consumo: ate 90 kWh nao paga, de 91 a 200 kWh paga 12% "
                f"e acima de 200 kWh paga 18% sobre TODO o consumo. Com 200 kWh o kWh sai por cerca de {reais(c.tarifa_final(200, P))}; "
                f"com 201 kWh, por {reais(c.tarifa_final(201, P))}. Quem esta um pouco acima de 200 kWh ganha muito ao economizar.",
                ["icms_faixas", "tarifa_tusd", "tarifa_te", "pis_cofins"])
    if t("tarifa", "kwh", "preco da energia", "preco da luz", "quanto custa a energia", "quanto custa a luz", "valor da luz", "bandeira", "enel"):
        return (f"Na Enel SP a tarifa residencial e de {reais(P['tarifa_tusd'] + P['tarifa_te'])} por kWh sem impostos "
                f"(vale de 04/07/2026 a 03/07/2027). Com impostos fica entre {reais(c.tarifa_final(150, P))} e "
                f"{reais(c.tarifa_final(250, P))}, conforme o consumo. A bandeira tarifaria (verde, amarela ou vermelha) muda "
                f"todo mes e pode somar um valor extra: confira na sua conta ou no site da ANEEL.",
                ["tarifa_tusd", "tarifa_te", "pis_cofins", "icms_faixas"])
    if t("co2", "ambiente", "poluic", "carbono", "sustent", "clima", "planeta", "natureza", "verde"):
        return (f"Cada kWh que deixa de vir da rede evita em media {num(P['fator_emissao_sin'] * 1000, 1)} g de CO2 "
                f"(fator medio do sistema eletrico brasileiro em 2025). Economizar 40 kWh por mes evita cerca de "
                f"{num(40 * 12 * P['fator_emissao_sin'], 0)} kg de CO2 por ano. A rede brasileira ja e bastante renovavel, "
                f"entao o maior ganho ambiental e reduzir desperdicio e aliviar a rede nos horarios de pico.",
                ["fator_emissao_sin"])
    palavras = set(q.replace("?", " ").replace(",", " ").replace(".", " ").split())
    if ({"conta", "luz", "energia"} & palavras) and ({"cara", "caro", "alta", "alto", "subiu", "aumentou"} & palavras):
        q += " conta alta"
    if t("economizar", "economia", "economizo", "diminuir", "reduzir", "baixar", "conta alta", "conta cara", "conta de luz", "pagar menos", "gastar menos", "dica", "ajuda"):
        return ("Tres acoes baratas, em ordem de resultado: (1) banho mais curto e chave no 'verao' quando der; "
                "(2) trocar por LED as lampadas que ficam mais tempo acesas; (3) cortar o stand-by com uma regua. "
                "Use a opcao 2 do menu para ver quanto isso da na SUA conta.", [])
    return (None, [])
