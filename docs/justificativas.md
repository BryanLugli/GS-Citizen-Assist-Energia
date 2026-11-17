# Justificativas das recomendações

Os números abaixo vêm de `analise/comparacao_alternativas.md` (casa de referência, 10 anos, Enel SP).

## Por que a recomendação é "eficiência primeiro, solar depois"

| Critério | Eficiência (hábitos + LED) | Solar fotovoltaica | Eficiência + solar |
|---|---|---|---|
| **Custo inicial** | R$ 78,90 | R$ 5.973 | R$ 4.061 |
| **Conta no 1º ano** | R$ 181/mês (−23%) | R$ 66/mês (−72%) | R$ 79/mês (−67%) |
| **Retorno** | ≈ 1 mês | ≈ 3,0 anos | ≈ 2,2 anos |
| **Custo total em 10 anos** | R$ 21,9 mil | R$ 14,7 mil | R$ 14,1 mil (menor) |
| **Viabilidade** | Qualquer casa, inclusive alugada e apartamento; depende de mudar hábito | Exige telhado próprio, sem sombra, ≈ 8 m², e capital ou financiamento | Mesmas exigências do solar, com sistema menor (≈ 5 m²) |
| **Impacto ambiental** | Evita ≈ 22 kg CO₂/ano; reduz a demanda no horário de pico (banho) | Evita ≈ 97 kg CO₂/ano; fonte renovável; gera resíduo eletrônico no fim da vida | Evita ≈ 87 kg CO₂/ano com menos material fabricado |
| **Principal limitação** | Economia depende de manter o hábito; parte do ganho vem da faixa do ICMS | Conta não zera (mínimo faturado + Fio B); geração varia com clima e telhado | Sistemas abaixo de 2 kWp podem custar mais por Wp |

1. **A eficiência tem o melhor retorno por real investido** e está ao alcance de todo o público, por isso é sempre o primeiro passo.
2. **O solar é o que mais reduz a conta**, mas só para quem tem telhado próprio e dinheiro; para os demais o assistente não o recomenda.
3. **Combinar os dois dá o menor custo total em 10 anos**: reduzir o consumo antes permite comprar um sistema menor.
4. **Trocar a geladeira não entra no pacote**: economiza cerca de 30 kWh/mês, mas custa cerca de R$ 2.599 e levaria cerca de 7 anos para se pagar.

Essa lógica está programada em `energia/calculos.py`, função `recomendar()`: a eficiência é sempre indicada; o solar só é indicado se o usuário declarar telhado próprio sem sombra, se o retorno for de até 6 anos e se a economia líquida superar a da eficiência sozinha.

## Como a análise aparece nas respostas do assistente

| Resultado da análise | Onde aparece no assistente |
|---|---|
| Consumo por equipamento (chuveiro = 38%) | Opção 1 e resposta sobre chuveiro/banho |
| Tabela comparativa das 4 alternativas | Opção 2, recalculada com o consumo que o usuário informa |
| Regra de recomendação | Opção 2, bloco "O que recomendamos" |
| Efeito do ICMS em 200 kWh | Resposta sobre impostos/tarifa |
| Fio B e conta que não zera | Opção 2 e resposta sobre Fio B |
| CO₂ evitado | Coluna da comparação e resposta sobre meio ambiente |
| Fontes e limitações | Mostradas junto de cada resposta e na opção 5 |

## Premissas e simplificações (o que pode fazer o resultado real ser diferente)

- **Tarifa**: Enel SP, bandeira verde, sem contribuição de iluminação pública; PIS/COFINS fixo em 6%.
- **ICMS com solar**: a faixa foi definida pela energia retirada da rede (premissa conservadora). A regra real de incidência sobre a energia compensada pode diferir.
- **Fio B**: valor estimado (R$ 0,15/kWh), cobrado sem tributos; depois de 2028 adotamos 100% (a regra ainda será definida pela ANEEL).
- **Geração solar**: média anual, sem sazonalidade, sombra ou orientação do telhado; degradação de 0,5% ao ano.
- **Simultaneidade de 30%**: família fora de casa durante o dia. Quem usa mais energia de dia paga menos Fio B.
- **Dinheiro**: valores de hoje, sem inflação da tarifa (que favoreceria o solar) e sem juros de financiamento ou troca de inversor (que o prejudicariam).
- **CO₂**: fator médio da rede; não inclui a fabricação e o descarte dos equipamentos.
- **Casa de referência**: potências e tempos de uso são estimativas do grupo, não medições.

A análise de sensibilidade (seção 7 do relatório) mostra que, variando Fio B, simultaneidade e irradiação, o retorno do solar fica entre 2,9 e 3,2 anos — a conclusão se mantém, mas o valor exato não é garantido.
