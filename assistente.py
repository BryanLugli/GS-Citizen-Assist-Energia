"""Citizen Assist AI - modulo de Energia (uso consciente e energia solar em casa).

Uso:
    python assistente.py            -> modo interativo (menu)
    python assistente.py --demo     -> mostra a analise completa da casa de referencia e sai

So usa a biblioteca padrao do Python (nao precisa instalar nada).
"""
import sys

from energia import calculos as c
from energia import respostas as r
from energia.dados import carregar_casa, carregar_premissas

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

LINHA = "-" * 105


class Sair(Exception):
    pass


def ler(texto):
    try:
        return input(texto).strip()
    except (EOFError, KeyboardInterrupt):
        raise Sair


def ler_numero(texto, minimo, maximo, padrao=None, inteiro=False):
    """Pede um numero ate o usuario digitar um valor valido (aceita virgula)."""
    while True:
        dica = f" [Enter = {padrao:g}]" if padrao is not None else ""
        bruto = ler(f"{texto}{dica}: ")
        if bruto == "" and padrao is not None:
            return padrao
        try:
            v = float(bruto.replace(",", "."))
            if inteiro and v != int(v):
                raise ValueError
        except ValueError:
            print(f"  Nao entendi '{bruto}'. Digite apenas um numero{' inteiro' if inteiro else ''}.")
            continue
        if not minimo <= v <= maximo:
            print(f"  O valor deve ficar entre {minimo:g} e {maximo:g}.")
            continue
        return int(v) if inteiro else v


def ler_opcao(texto, opcoes):
    while True:
        v = ler(texto).lower()
        if v in opcoes:
            return opcoes[v]
        print("  Opcao invalida. Escolha: " + ", ".join(opcoes))


def mostrar_casa(P):
    casa = carregar_casa()
    itens, total = c.consumo_casa(casa)
    print("\nONDE VAI A ENERGIA - casa de referencia (4 pessoas, Grande Sao Paulo; dados ESTIMADOS pelo grupo)")
    print(LINHA)
    for nome, kwh in itens:
        barra = "#" * round(kwh / total * 50)
        print(f"{nome:<40}{r.num(kwh):>8} kWh/mes {kwh / total * 100:>5.1f}%  {barra}")
    print(f"{'TOTAL':<40}{r.num(total):>8} kWh/mes   (media das casas brasileiras: "
          f"{r.num(P['consumo_medio_residencial_br'])} kWh/mes - EPE, ago/2026)")
    print(f"Conta estimada: {r.reais(c.conta_mensal(total, P))} por mes.")
    return total


def simular(P, meta, consumo=None, demo=False):
    if consumo is None:
        print("\nSIMULACAO COM A SUA CONTA  (olhe o campo 'consumo em kWh' da sua fatura; nao pedimos nome nem endereco)")
        consumo = ler_numero("Consumo do mes em kWh", 30, 2000)
    if demo:
        lig, pessoas, m_at, m_nv, lamp, pode = "bifasica", 4, 8, 6, 8, True
    else:
        lig = ler_opcao("Tipo de ligacao - (m)onofasica, (b)ifasica ou (t)rifasica? Se nao souber, digite b: ",
                        {"m": "monofasica", "b": "bifasica", "t": "trifasica"})
        pessoas = ler_numero("Quantas pessoas tomam banho de chuveiro eletrico", 0, 20, 4, inteiro=True)
        m_at = ler_numero("Quantos minutos dura cada banho, em media", 1, 60, 8)
        m_nv = ler_numero("Para quantos minutos da para reduzir", 1, m_at, min(6, m_at))
        lamp = ler_numero("Quantas lampadas da casa ainda NAO sao LED", 0, 100, 0, inteiro=True)
        pode = ler_opcao("A casa e propria e tem telhado sem sombra? (s/n): ", {"s": True, "n": False})
    medidas, econ, invest = c.pacote_eficiencia(P, pessoas, m_at, m_nv, n_lampadas=lamp)
    if econ > consumo * 0.6:
        print("  Atencao: a economia calculada passou de 60% do consumo informado; limitamos a 60%. Confira os dados digitados.")
        econ = consumo * 0.6
    cen = c.comparar(consumo, econ, invest, P, lig)
    print("\n" + LINHA)
    print(f"Consumo informado: {r.num(consumo)} kWh/mes | conta estimada hoje: {r.reais(cen[0]['conta_mes_ano1'])}")
    print("Medidas de eficiencia consideradas:")
    for nome, kwh, custo in medidas:
        print(f"  - {nome}: economiza {r.num(kwh)} kWh/mes, custa {r.reais(custo)}")
    print("\nCOMPARACAO (mesma casa, mesmo periodo de " + str(cen[0]["horizonte"]) + " anos):")
    print(r.texto_comparacao(cen, P))
    print("\n" + r.texto_recomendacao(cen, P, pode))
    print("\nCondicoes e limites desta estimativa:")
    for lim in r.LIMITACOES:
        print("  - " + lim)
    print("Principais fontes:")
    print(r.fontes_usadas(meta, ["tarifa_tusd", "icms_faixas", "preco_fv_4kwp", "fio_b_percentual",
                                 "irradiacao_hsp", "fator_emissao_sin"]))
    print(LINHA)
    return cen


def um_aparelho(P):
    print("\nQUANTO GASTA UM APARELHO  (a potencia em watts esta na etiqueta do aparelho)")
    w = ler_numero("Potencia em watts (W)", 1, 20000)
    h = ler_numero("Horas de uso por dia", 0.01, 24)
    d = ler_numero("Dias de uso por mes", 1, 31, 30, inteiro=True)
    kwh = c.kwh_equipamento(w, h, d)
    print(f"  Conta: {w:g} W / 1000 x {h:g} h x {d} dias = {r.num(kwh)} kWh por mes, "
          f"cerca de {r.reais(kwh * c.tarifa_final(250, P))} (tarifa Enel SP com impostos, estimativa).")


def perguntar(P, meta):
    print("\nPERGUNTE  (ex.: 'vale a pena placa solar?', 'o que e fio B?', 'como economizar no banho?'). Enter vazio volta ao menu.")
    while True:
        q = ler("Sua pergunta: ")
        if not q:
            return
        resp, chaves = r.responder(q, P, meta)
        if resp is None:
            print("  Ainda nao sei responder isso. Temas que conheco: chuveiro, lampadas LED, stand-by, geladeira, "
                  "tarifa e impostos, energia solar, Fio B, meio ambiente.")
            continue
        print("  " + resp)
        if chaves:
            print("  Fontes:\n" + r.fontes_usadas(meta, chaves))
        print("  (estimativa; veja a opcao 5 para condicoes e limites)")


def fontes(meta):
    print("\nFONTES E PREMISSAS  (REAL = publicado; ESTIMADO = premissa do grupo)")
    print(r.fontes_usadas(meta, list(meta)))
    print("\nLIMITACOES")
    for lim in r.LIMITACOES:
        print("  - " + lim)


def main():
    P, meta = carregar_premissas()
    print("=" * 105)
    print(" CITIZEN ASSIST AI - Energia: como gastar menos luz em casa e quando a energia solar vale a pena")
    print("=" * 105)
    print(r.AVISO)
    if "--demo" in sys.argv:
        total = mostrar_casa(P)
        simular(P, meta, consumo=total, demo=True)
        return 0
    try:
        while True:
            print("\n 1 - Ver onde vai a energia de uma casa\n 2 - Simular com a minha conta (economia x energia solar)\n"
                  " 3 - Calcular o gasto de um aparelho\n 4 - Fazer uma pergunta\n 5 - Fontes e limitacoes\n 0 - Sair")
            op = ler("Escolha: ")
            if op == "1":
                mostrar_casa(P)
            elif op == "2":
                simular(P, meta)
            elif op == "3":
                um_aparelho(P)
            elif op == "4":
                perguntar(P, meta)
            elif op == "5":
                fontes(meta)
            elif op == "0":
                break
            else:
                print("  Opcao invalida. Digite um numero de 0 a 5.")
    except Sair:
        pass
    print("\nAtendimento encerrado. Nenhum dado foi guardado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
