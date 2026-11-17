# Análise de consumo e comparação das alternativas

> Arquivo gerado por `analise/gerar_relatorio.py`. Todos os números saem de `dados/premissas.json` e `dados/casa_referencia.csv`. Valores marcados como **estimado** são premissas do grupo, não medições.

## 1. Necessidade analisada

Abastecer com eletricidade, durante 10 anos (2027 a 2036), uma casa de 4 pessoas na área da Enel SP, gastando menos e com menor impacto ambiental. As quatro alternativas atendem **a mesma casa no mesmo período**.

## 2. Análise de consumo (casa de referência — dados estimados)

Fórmula: `kWh/mês = potência (W) ÷ 1000 × horas por dia × dias por mês × quantidade`

| Equipamento | Qtd | Potência (W) | h/dia | dias/mês | kWh/mês | % |
|---|---:|---:|---:|---:|---:|---:|
| Chuveiro eletrico | 1 | 5500 | 0,53 | 30 | 88,0 | 38,2 |
| Geladeira frost free 2 portas (antiga) | 1 | — | — | — | 55,0 | 23,9 |
| Lampada fluorescente compacta | 8 | 20 | 5 | 30 | 24,0 | 10,4 |
| TV LED 42 pol | 1 | 100 | 5 | 30 | 15,0 | 6,5 |
| Ventilador | 1 | 80 | 6 | 30 | 14,4 | 6,3 |
| Computador/notebook | 1 | 60 | 6 | 30 | 10,8 | 4,7 |
| Aparelhos em stand-by | 1 | 10 | 24 | 30 | 7,2 | 3,1 |
| Micro-ondas | 1 | 1200 | 0,17 | 30 | 6,0 | 2,6 |
| Maquina de lavar roupa | 1 | 500 | 1 | 12 | 6,0 | 2,6 |
| Ferro de passar | 1 | 1000 | 1 | 4 | 4,0 | 1,7 |
| **Total** | | | | | **230,4** | 100 |

Comparação com dado real: o consumo residencial médio no Brasil foi de 181,8 kWh/mês em agosto/2026 (EPE). A casa de referência fica acima da média porque tem 4 moradores e chuveiro elétrico.

### Conta de luz

- Tarifa sem tributos (ANEEL, REH 3.596/2026): 0,47242 + 0,31696 = **R$ 0,78938/kWh**
- Com tributos: `tarifa ÷ (1 − PIS/COFINS) ÷ (1 − ICMS)` → acima de 200 kWh (ICMS 18%): **R$ 1,0241/kWh**; de 91 a 200 kWh (ICMS 12%): **R$ 0,9543/kWh**
- Conta atual: 230,4 kWh × R$ 1,0241 = **R$ 235,95 por mês**

## 3. Alternativa 1 — Eficiência energética (hábitos + LED)

| Medida | Economia (kWh/mês) | Custo |
|---|---:|---:|
| Banho de 8 para 6 min (4 pessoas) | 22,0 | R$ 0,00 |
| Trocar 8 lampadas de 20 W por LED 9 W | 13,2 | R$ 50,40 |
| Regua com interruptor para cortar 70% do stand-by | 5,0 | R$ 28,50 |
| **Total** | **40,2** | **R$ 78,90** |

Novo consumo: 230,4 − 40,2 = **190,2 kWh/mês**. Como fica abaixo de 200 kWh, o ICMS cai de 18% para 12%: 190,2 × R$ 0,9543 = **R$ 181,46 por mês**.

Atenção: da economia de R$ 54,49/mês, cerca de R$ 41,21 vêm dos kWh economizados e o restante da mudança de faixa do ICMS. Numa casa que já consome menos de 200 kWh (ou muito mais), esse segundo ganho não existe.

Medida opcional analisada à parte — geladeira nova eficiente (55 → 24,9 kWh/mês): economiza 30,1 kWh/mês (≈ R$ 30,83), custa cerca de R$ 2.599,00 e levaria ≈ 7 anos para se pagar. Não entra no pacote: só compensa quando a antiga precisa ser trocada.

## 4. Alternativa 2 — Energia solar fotovoltaica (fonte renovável)

- Geração por kWp: 4,5 kWh/m²·dia × 365 ÷ 12 × 0,78 = **106,8 kWh/kWp·mês**
- Energia a compensar: 230,4 − 50 (mínimo faturado, ligação bifásica) = 180,4 kWh → 3 módulos de 550 Wp = **1,65 kWp**, gerando **176,2 kWh/mês** (≈ 8 m² de telhado)
- Investimento: 1650 Wp × R$ 3,62/Wp = **R$ 5.973,00**
- Conta no 1º ano (2027): consumida na hora 52,8 kWh; injetada 123,3 kWh; retirada da rede 177,5 kWh; compensada 123,3 kWh; faturada 54,2 kWh
- Valor: 54,2 × R$ 0,9543 + 123,3 × R$ 0,15 × 75% (Fio B) = **R$ 65,63 por mês**

## 5. Alternativa 3 — Eficiência + solar

Primeiro reduz o consumo para 190,2 kWh/mês e só depois dimensiona o sistema: 2 módulos (1,10 kWp), R$ 3.982,00 + R$ 78,90 das medidas = **R$ 4.060,90**. Conta no 1º ano: **R$ 78,64 por mês**. Sistemas abaixo de 2 kWp são pouco comuns no mercado e tendem a custar mais por Wp que a referência usada; por isso este valor deve ser confirmado com orçamentos.

## 6. Comparação (10 anos, valores de hoje, sem inflação nem juros)

| Alternativa | Renovável | Conta/mês (1º ano) | Investimento | Retorno | Custo total em 10 anos | Economia líquida | CO₂ evitado/ano |
|---|:-:|---:|---:|---:|---:|---:|---:|
| Situacao atual | não | R$ 235,95 | R$ 0,00 | — | R$ 28.313,92 | R$ 0,00 | 0 kg |
| Eficiencia (habitos + LED) | não | R$ 181,46 | R$ 78,90 | 1 mês | R$ 21.854,30 | R$ 6.459,62 | 22 kg |
| Solar fotovoltaica | sim | R$ 65,63 | R$ 5.973,00 | 3,0 anos | R$ 14.724,56 | R$ 13.589,37 | 97 kg |
| Eficiencia + solar | sim | R$ 78,64 | R$ 4.060,90 | 2,2 anos | R$ 14.081,72 | R$ 14.232,20 | 87 kg |

CO₂ evitado = kWh que deixam de vir da rede × 0,0461 tCO₂/MWh (fator médio do SIN em 2025, MCTI). Como a rede brasileira já é majoritariamente renovável, o valor em kg é pequeno; não inclui as emissões de fabricação dos módulos.

## 7. Análise de sensibilidade do cenário solar (premissas estimadas)

| Fio B (R$/kWh) | Conta/mês (1º ano) | Retorno (anos) | Economia líquida em 10 anos |
|---:|---:|---:|---:|
| 0,10 | R$ 61,01 | 2,9 | R$ 14.286,95 |
| 0,15 | R$ 65,63 | 3,0 | R$ 13.589,37 |
| 0,20 | R$ 70,25 | 3,1 | R$ 12.891,79 |
| 0,25 | R$ 74,88 | 3,2 | R$ 12.194,21 |

| Simultaneidade | Conta/mês (1º ano) | Retorno (anos) | Economia líquida em 10 anos |
|---:|---:|---:|---:|
| 0,15 | R$ 72,39 | 3,1 | R$ 12.653,69 |
| 0,30 | R$ 65,63 | 3,0 | R$ 13.589,37 |
| 0,45 | R$ 62,66 | 2,9 | R$ 14.037,81 |

| Irradiação (kWh/m²·dia) | Conta/mês (1º ano) | Retorno (anos) | Economia líquida em 10 anos |
|---:|---:|---:|---:|
| 4,2 | R$ 75,91 | 3,2 | R$ 12.413,91 |
| 4,5 | R$ 65,63 | 3,0 | R$ 13.589,37 |
| 4,8 | R$ 61,67 | 2,9 | R$ 14.430,90 |

Leitura: mesmo no pior caso testado o sistema se paga dentro do período, mas o retorno muda — por isso o assistente apresenta os números como estimativa e orienta a pedir simulação com a conta real.
