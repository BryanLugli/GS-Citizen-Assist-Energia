# Referências

Todas as fontes foram consultadas em **16/11/2026**. A coluna "Usado em" indica a chave correspondente em `dados/premissas.json`.

| # | Fonte | O que foi usado | Usado em |
|---|---|---|---|
| 1 | ANEEL. Resolução Homologatória nº 3.596, de 30/06/2026 (Reajuste Tarifário Anual da Enel SP). Tabela publicada pela distribuidora: https://www.enel.com.br/pt-saopaulo/Para_Voce/tarifa-energia-eletrica.html | Tarifa B1 residencial: TUSD 472,42 R$/MWh e TE 316,96 R$/MWh, válidas a partir de 04/07/2026 | `tarifa_tusd`, `tarifa_te` |
| 2 | Calculadora do Mundo. "Enel SP 2026: tarifa e valor do kWh em São Paulo" (cita a REH 3.596/2026 e o RICMS/2000-SP, art. 52, V): https://www.calculadoradomundo.com.br/energia/tarifa-energia-por-distribuidora/enel-sp | Faixas de ICMS residencial em SP, faixa usual de PIS/COFINS, custo de disponibilidade e valor de conferência (R$ 0,9543/kWh a 200 kWh) | `icms_faixas`, `pis_cofins`, `disponibilidade_kwh` |
| 3 | EPE. Resenha Mensal do Mercado de Energia Elétrica (agosto/2026), divulgada por Brasil 61: https://brasil61.com/n/impulsionado-pelo-el-nino-consumo-de-eletricidade-residencial-bate-recorde-historico-em-agosto-bras2617205 | Consumo residencial médio de 181,8 kWh/mês | `consumo_medio_residencial_br` |
| 4 | Brasil. Lei nº 14.300/2022 (Marco Legal da Geração Distribuída), art. 27: https://www.legjur.com/legislacao/art/lei_00143002022-27 — e Canal Solar, "Consumidores passarão a arcar com 60% do Fio B a partir de 2026": https://canalsolar.com.br/consumidores-60-do-fio-b-2026/ | Cronograma de cobrança do Fio B sobre a energia compensada (15% em 2023 … 60% em 2026, 75% em 2027, 90% em 2028) | `fio_b_percentual` |
| 5 | Greener. Estudo Estratégico Soluções Energéticas Distribuídas, 1º semestre/2026, divulgado por pv magazine Brasil (25/09/2026): https://www.pv-magazine-brasil.com/2026/09/25/sistemas-fotovoltaicos-ficam-ate-7-mais-caros-no-1o-semestre-de-2026-aponta-greener/ | Preço final de sistemas fotovoltaicos: R$ 3,62/Wp (2 kWp) e R$ 2,91/Wp (4 kWp), junho/2026 | `preco_fv_2kwp`, `preco_fv_4kwp` |
| 6 | MCTI/SIRENE. Fatores de emissão de CO₂ do Sistema Interligado Nacional — fator médio para inventários: https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao | Fator médio anual de 2025: 0,0461 tCO₂/MWh | `fator_emissao_sin` |
| 7 | CRESESB/CEPEL. Programa SunData (irradiação solar diária média por localidade): https://cresesb.cepel.br/sundata/index.php | Ferramenta indicada para conferir a irradiação do endereço; o valor de 4,5 kWh/m²·dia é premissa conservadora do grupo | `irradiacao_hsp` |
| 9 | Levantamento de preços em lojas on-line (17/11/2026): Magazine Luiza https://www.magazineluiza.com.br/busca/lampada+de+led+9w/ · Amazon https://www.amazon.com.br/led-9w/s?k=led+9w · Mercado Livre https://lista.mercadolivre.com.br/filtro-com-interruptor-individual · Amazon https://www.amazon.com.br/Filtro-Linha-Tomadas-Interruptor-Branco/dp/B0H8PZG3BZ | Lâmpada LED 9 W (mediana R$ 6,30) e filtro de linha com interruptor (mediana R$ 28,50) | `custo_lampada_led`, `custo_regua` |
| 10 | NerdAnalisa. "Melhor geladeira frost free: as 7 melhores em 2026": https://nerdanalisa.com.br/melhor-geladeira-frost-free/ | Consul Inverter CRM44MB: R$ 2.599 e 24,9 kWh/mês | `custo_geladeira_nova`, `consumo_geladeira_nova` |
| 8 | Custo Solar. "Irradiação solar por estado do Brasil" (base: Atlas Brasileiro de Energia Solar/INPE): https://custosolar.com/irradiacao/sao-paulo | Média estadual de SP (4,8 kWh/m²·dia) e taxa de desempenho de 80% usadas como comparação | `irradiacao_hsp`, `taxa_desempenho` |

## Pontos que o grupo deve conferir antes da entrega

O enunciado responsabiliza a equipe pela verificação dos dados. Abra cada link e confirme:

1. **Fator de emissão (item 6)** — o valor 0,0461 foi obtido de publicações que citam a planilha do MCTI; abra a planilha "Fator médio – Inventários corporativos" e confirme a média anual de 2025.
2. **Fio B da Enel SP** — as fontes encontradas divergem (de R$ 0,10 a R$ 0,25/kWh). O valor de R$ 0,15 é estimado; se encontrarem o valor oficial na tabela de componentes da REH 3.596/2026, troquem em `dados/premissas.json` e rodem `python analise/gerar_relatorio.py`.
3. **Irradiação (item 7)** — consultar São Paulo no SunData e anotar o valor do plano inclinado.
4. **Preços de LED, régua e geladeira** — levantados em 17/11/2026 (itens 9 e 10). Preço de loja muda rápido: abram os links e confirmem que continuam próximos.
5. **Consumo da geladeira antiga (55 kWh/mês)** — é estimativa; se alguém tiver uma geladeira antiga em casa, vejam a etiqueta.
