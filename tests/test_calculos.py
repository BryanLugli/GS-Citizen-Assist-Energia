"""Testes automaticos dos calculos.  Rodar:  python -m unittest discover -s tests -v"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from energia import calculos as c
from energia import respostas as r
from energia.dados import carregar_casa, carregar_premissas

P, META = carregar_premissas()


class TestConsumo(unittest.TestCase):
    def test_chuveiro(self):
        # 5500 W, 30 min por dia, 30 dias = 82,5 kWh
        self.assertAlmostEqual(c.kwh_equipamento(5500, 0.5, 30), 82.5)

    def test_entrada_invalida(self):
        with self.assertRaises(ValueError):
            c.kwh_equipamento(-100, 1)
        with self.assertRaises(ValueError):
            c.kwh_equipamento(100, 25)

    def test_casa_referencia(self):
        itens, total = c.consumo_casa(carregar_casa())
        self.assertAlmostEqual(total, 230.4, places=1)
        self.assertEqual(itens[0][0], "Chuveiro eletrico")


class TestConta(unittest.TestCase):
    def test_tarifa_200kwh_confere_com_fonte(self):
        # a fonte consultada informa R$ 0,9543/kWh com tributos para 200 kWh
        self.assertAlmostEqual(c.tarifa_final(200, P), 0.9543, places=4)

    def test_faixas_icms(self):
        self.assertEqual(c.aliquota_icms(90, P), 0.0)
        self.assertEqual(c.aliquota_icms(200, P), 0.12)
        self.assertEqual(c.aliquota_icms(201, P), 0.18)

    def test_minimo_faturado(self):
        self.assertAlmostEqual(c.conta_mensal(10, P, "bifasica"), 50 * c.tarifa_final(10, P))


class TestSolar(unittest.TestCase):
    def test_geracao_por_kwp(self):
        self.assertAlmostEqual(c.geracao_por_kwp(P), 4.5 * 365 / 12 * 0.78)

    def test_preco_interpolado(self):
        self.assertEqual(c.preco_por_wp(1, P), 3.62)
        self.assertEqual(c.preco_por_wp(5, P), 2.91)
        self.assertAlmostEqual(c.preco_por_wp(3, P), (3.62 + 2.91) / 2)

    def test_balanco_de_energia(self):
        d = c.conta_com_fv(230.4, 176.2, 2027, P)
        self.assertAlmostEqual(d["autoconsumo"] + d["injetado"], 176.2)
        self.assertAlmostEqual(d["rede"] - d["compensado"], d["faturado"])
        self.assertGreaterEqual(d["faturado"], 50)

    def test_conta_nunca_zera(self):
        d = c.conta_com_fv(200, 1000, 2027, P)
        self.assertGreater(d["valor"], 0)
        self.assertEqual(d["faturado"], 50)

    def test_fio_b_cresce(self):
        v = [c.conta_com_fv(230.4, 176.2, a, P)["valor"] for a in (2026, 2027, 2028, 2029)]
        self.assertEqual(v, sorted(v))


class TestComparacao(unittest.TestCase):
    def setUp(self):
        _, self.econ, self.inv = c.pacote_eficiencia(P)
        self.cen = c.comparar(230.4, self.econ, self.inv, P)

    def test_quatro_cenarios_com_renovavel(self):
        self.assertEqual(len(self.cen), 4)
        self.assertTrue(any(x["renovavel"] for x in self.cen))

    def test_todas_alternativas_reduzem_a_conta(self):
        for x in self.cen[1:]:
            self.assertLess(x["conta_mes_ano1"], self.cen[0]["conta_mes_ano1"])

    def test_custo_total_coerente(self):
        base = self.cen[0]
        self.assertAlmostEqual(base["custo_total"], base["conta_mes_ano1"] * 12 * base["horizonte"])

    def test_recomendacao_sem_telhado_e_eficiencia(self):
        escolhido, _ = c.recomendar(self.cen, pode_instalar_fv=False)
        self.assertFalse(escolhido["renovavel"])


class TestRespostas(unittest.TestCase):
    def test_perguntas_conhecidas(self):
        for q in ["Vale a pena placa solar?", "o que é fio B", "como economizar no banho",
                  "lâmpada LED compensa?", "moro de aluguel, posso por painel solar?", "quanto custa o kWh"]:
            resp, _ = r.responder(q, P, META)
            self.assertIsNotNone(resp, q)

    def test_perguntas_sem_palavra_chave_e_por_numero(self):
        # ajuste feito apos o teste com o Participante 1
        for q in ["minha conta ta muito cara", "o que gasta mais em casa?", "quero gerar minha propria energia",
                  "por que a conta nao zera?", "1", "8", str(len(r.TEMAS))]:
            self.assertIsNotNone(r.responder(q, P, META)[0], q)
        self.assertIsNone(r.responder("99", P, META)[0])

    def test_pergunta_desconhecida(self):
        self.assertIsNone(r.responder("qual o resultado do jogo de ontem", P, META)[0])

    def test_resumo_curto(self):
        # Ajuste do teste com o Participante 2: o resumo mostrado primeiro tem poucas linhas
        P, _ = carregar_premissas()
        cen = c.comparar(230.4, 40.2, 78.9, P, "bifasica")
        resumo = r.texto_resumo(cen, P, True)
        self.assertLessEqual(len(resumo.splitlines()), 6)
        self.assertIn("R$", resumo)

    def test_solar_explica_como_baratear(self):
        # Ajuste do teste com o Participante 3: achou as placas caras
        P, meta = carregar_premissas()
        resp, _ = r.responder("vale a pena colocar placa solar?", P, meta)
        self.assertIn("mais barato", resp)
        self.assertIn("orcamentos", resp)

    def test_fontes_existem(self):
        for q in ["fio b", "placa solar", "led", "co2"]:
            _, chaves = r.responder(q, P, META)
            for k in chaves:
                self.assertIn(k, META)

    def test_toda_premissa_tem_fonte_e_tipo(self):
        for k, m in META.items():
            self.assertIn(m["tipo"], ("real", "estimado"), k)
            self.assertTrue(m["fonte"], k)


if __name__ == "__main__":
    unittest.main()
