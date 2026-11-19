# Citizen Assist AI — Energia em casa

**Global Solution 2026.2 · FIAP · Ciência da Computação (1CCPY)**
**Disciplina: Soluções em Energias Renováveis e Sustentáveis**

Módulo de energia do assistente digital Citizen Assist AI: mostra onde a casa gasta eletricidade, compara **economizar (eficiência)** com **gerar a própria energia (solar fotovoltaica)** e explica o resultado em linguagem simples, com fontes e limitações.

## Integrantes

| Nome | RM |
|---|---|
| Beckman Rodrigues Lugli | 573442 |
| Bryan Vinicius Rodrigues Lugli | 571350 |
| Guilherme Xavier | 573053 |

## Público e problema

- **Público:** famílias que moram em casas na Grande São Paulo (área da Enel SP) e pagam a própria conta de luz.
- **Necessidade energética:** a tarifa residencial subiu em julho/2026 e o consumo médio das casas brasileiras bateu recorde (181,8 kWh/mês, EPE). A família quer saber **o que fazer primeiro para pagar menos** e **se vale a pena instalar placas solares**, mas as informações disponíveis são técnicas ou vêm de quem quer vender o sistema.
- **Como o assistente ajuda:** calcula com a conta da própria pessoa, compara as alternativas no mesmo período, recomenda uma ordem de ação e deixa claro o que é estimativa.

## Funcionalidades de energia

| Opção do menu | O que faz |
|---|---|
| 1 — Onde vai a energia | Consumo por equipamento de uma casa de referência (kWh e %) |
| 2 — Simular com a minha conta | Compara situação atual, eficiência, solar e eficiência + solar: conta mensal, investimento, retorno, custo em 10 anos e CO₂ evitado; termina com uma recomendação |
| 3 — Gasto de um aparelho | Converte potência (W) e tempo de uso em kWh e reais |
| 4 — Fazer uma pergunta | Responde dúvidas escritas com as palavras do usuário ou escolhidas por número numa lista de 11 temas (chuveiro, LED, stand-by, geladeira, tarifa e impostos, solar, Fio B, meio ambiente), citando as fontes |
| 5 — Fontes e limitações | Lista todas as premissas, marcadas como REAL ou ESTIMADO |

O assistente trata entradas inválidas, não pede dados pessoais e avisa que não é canal oficial.

## Resultado da análise (casa de referência, 10 anos)

| Alternativa | Conta/mês (1º ano) | Investimento | Retorno | Custo total em 10 anos | CO₂ evitado/ano |
|---|---:|---:|---:|---:|---:|
| Situação atual (230,4 kWh/mês) | R$ 235,95 | — | — | R$ 28.313,92 | — |
| Eficiência (hábitos + LED) | R$ 181,46 | R$ 78,90 | 1 mês | R$ 21.854,30 | 22 kg |
| Solar fotovoltaica (renovável) | R$ 65,63 | R$ 5.973,00 | 3,0 anos | R$ 14.724,56 | 97 kg |
| Eficiência + solar (renovável) | R$ 78,64 | R$ 4.060,90 | 2,2 anos | R$ 14.081,72 | 87 kg |

**Recomendação:** começar pela eficiência (barata e possível para todos) e, havendo telhado próprio sem sombra e recursos, instalar o solar já dimensionado para o consumo reduzido. São estimativas — ver limitações em [`docs/justificativas.md`](docs/justificativas.md).

## Como executar

Requisito: Python 3.10 ou mais novo. **Não precisa instalar nenhuma biblioteca.**

```bash
python assistente.py                          # assistente interativo
python assistente.py --demo                   # análise completa da casa de referência
python analise/gerar_relatorio.py             # recria o relatório e o CSV de resultados
python -m unittest discover -s tests -v       # 20 testes automáticos
```

No PyCharm: abrir a pasta do projeto, clicar com o botão direito em `assistente.py` → **Run 'assistente'**.

## Onde está cada item pedido

| Item do enunciado | Arquivo |
|---|---|
| Códigos desenvolvidos | [`assistente.py`](assistente.py), [`energia/`](energia), [`analise/gerar_relatorio.py`](analise/gerar_relatorio.py), [`tests/`](tests) |
| Dados utilizados, origem e premissas | [`dados/premissas.json`](dados/premissas.json), [`dados/casa_referencia.csv`](dados/casa_referencia.csv) |
| Cálculos e comparação das alternativas | [`analise/comparacao_alternativas.md`](analise/comparacao_alternativas.md), [`analise/resultados.csv`](analise/resultados.csv) |
| Justificativas (custos, viabilidade, impactos ambientais) | [`docs/justificativas.md`](docs/justificativas.md) |
| Referências | [`docs/referencias.md`](docs/referencias.md) |
| Testes com usuários e ajustes | [`docs/testes_usuarios.md`](docs/testes_usuarios.md) |

## Conceitos da disciplina aplicados

- **Potência e energia:** kWh = W ÷ 1000 × h.
- **Eficiência energética:** mesma iluminação com 9 W em vez de 20 W; redução de tempo de uso e de stand-by.
- **Fonte renovável:** geração fotovoltaica = kWp × irradiação × taxa de desempenho; compensação de energia (Lei 14.300/2022).
- **Sustentabilidade:** emissões evitadas pelo fator médio do Sistema Interligado Nacional; análise de custo, viabilidade e limitações.

## Uso de IA generativa

Usamos IA generativa como apoio na pesquisa de fontes e na escrita do código e dos textos. As respostas do assistente **não** são geradas por IA em tempo de execução: saem de regras e cálculos rastreáveis no código. Os dados, as contas e as referências foram conferidos pelo grupo nas fontes listadas em `docs/referencias.md`.
