# Testes com usuários

Testes feitos com pessoas do público (adultos que pagam conta de luz). Para proteger a privacidade, não registramos nome, endereço nem número da instalação: cada pessoa aparece como "Participante 1", "Participante 2"…

## Registro dos testes

### Participante 1 — 17/11/2026 (presencial, no computador do grupo)

**Perfil:** adulto, mora em casa própria.

| Situação | Resultado |
|---|---|
| S1 — o que mais gasta | Identificou o **chuveiro** sem dificuldade. |
| S2 — simular com a conta | Conseguiu fazer a simulação. |
| S3 — o que faria primeiro | Respondeu que **economizaria** (eficiência) primeiro. |
| S4 — perguntar sobre placa solar | Entendeu a resposta. Durante a tarefa, notou que **o assistente só entendia quando a pergunta tinha certas palavras-chave**. |
| Navegação | Na tela de perguntas, **não conseguiu voltar ao menu**: digitou "0" e "fechar", e o assistente tratou as duas como perguntas que não entendia. |

| Pergunta final | Resposta |
|---|---|
| Fácil de entender (1–5) | **4** |
| Ajudaria a decidir (1–5) | **5** |
| Palavra que não entendeu | Nenhuma informada |
| Mudaria algum hábito? | "Economizaria junto com placas solares menores" — a mesma alternativa que a análise indica (eficiência + solar dimensionado para o consumo reduzido). |
| Sugestão | Relatou os dois problemas acima. |

### Participante 2 — 19/11/2026

**Perfil:** adulta.

| Situação | Resultado |
|---|---|
| S1 — o que mais gasta | Identificou o **chuveiro**. |
| S2 — simular com a conta | **Achou o kWh** na conta e fez a simulação. |
| S3 — o que faria primeiro | Respondeu que **economizaria** (eficiência) primeiro. |
| S4 — perguntar sobre placa solar | Entendeu a resposta: disse que **vale a pena, porque reduz muito a conta**. |
| S5 — gasto de um aparelho | **Conseguiu calcular**. |

| Pergunta final | Resposta |
|---|---|
| Fácil de entender (1–5) | **5** |
| Ajudaria a decidir (1–5) | **5** |
| Palavra que não entendeu | Nenhuma: entendeu tudo |
| O que faltou | **Os textos ficaram muito longos.** |

### Participante 3 — 19/11/2026

**Perfil:** adulta.

| Situação | Resultado |
|---|---|
| S1 — o que mais gasta | Identificou o **chuveiro**. |
| S2 — simular com a conta | **Achou o kWh** na conta e fez a simulação. |
| S3 — o que faria primeiro | Respondeu que **economizaria** (eficiência) primeiro. |
| S4 — perguntar sobre placa solar | Entendeu a resposta: disse que **vale a pena, porque reduz muito a conta**, mas que **as placas solares são um pouco caras**. |
| S5 — gasto de um aparelho | **Conseguiu calcular**. |

| Pergunta final | Resposta |
|---|---|
| Fácil de entender (1–5) | **5** |
| Ajudaria a decidir (1–5) | **5** |
| Palavra que não entendeu | Nenhuma: entendeu tudo |
| O que faltou | Nada além do custo das placas, comentado acima. |

## Ajustes realizados

| Problema observado | Quem relatou | Ajuste feito | Arquivo |
|---|---|---|---|
| Não conseguia sair da tela de perguntas: digitou "0" e "fechar" e o assistente não entendeu | Participante 1 | Passou a aceitar "0", "sair", "voltar", "fechar" e Enter vazio; aviso na tela explicando como voltar; "sair" e "fechar" também funcionam no menu principal | `assistente.py` |
| O assistente só entendia perguntas com palavras-chave específicas | Participante 1 | (1) Lista de 11 temas numerados exibida na tela de perguntas: o usuário pode digitar só o número; (2) mais sinônimos e frases do dia a dia ("minha conta tá muito cara", "o que gasta mais", "quero gerar minha própria energia", "por que a conta não zera"); (3) quando não entende, mostra a lista de temas em vez de só uma mensagem de erro; (4) novo teste automático com essas frases | `energia/respostas.py`, `assistente.py`, `tests/test_calculos.py` |
| Os textos ficaram muito longos | Participante 2 | A simulação (opção 2) agora mostra primeiro um **resumo de 5 linhas** (conta hoje, melhor opção, quanto a conta pode cair, investimento e primeiro passo) e pergunta se a pessoa quer ver os detalhes (tabela, limites e fontes). As respostas da opção 4 passaram a ser quebradas em linhas mais curtas. Novo teste automático confere que o resumo é curto | `energia/respostas.py`, `assistente.py`, `tests/test_calculos.py` |
| Achou as placas solares um pouco caras | Participante 3 | A resposta sobre placa solar (opção 4, tema 8) agora explica como deixar o sistema mais barato: economizar primeiro (com menos consumo, o sistema fica menor), pedir pelo menos 3 orçamentos e ver na opção 2 em quanto tempo o investimento se paga. Isso segue a recomendação da análise (eficiência primeiro, depois solar dimensionado para o consumo reduzido). Novo teste automático confere essa orientação | `energia/respostas.py`, `tests/test_calculos.py` |

## Verificações automáticas (não substituem o teste com pessoas)

`python -m unittest discover -s tests -v` — 22 testes: fórmulas de consumo, tarifa conferida com a fonte (R$ 0,9543/kWh a 200 kWh), faixas de ICMS, balanço de energia do solar, coerência da comparação, respostas com fonte, tratamento de entradas inválidas e reconhecimento de perguntas escritas com palavras do dia a dia (incluído após o teste com o Participante 1) e tamanho do resumo da simulação (incluído após o teste com o Participante 2) e orientação sobre o custo das placas (incluído após o teste com o Participante 3).
