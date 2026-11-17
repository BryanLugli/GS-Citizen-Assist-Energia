# Testes com usuários

Testes feitos com pessoas do público (adultos que pagam conta de luz). Para proteger a privacidade, não registramos nome, endereço nem número da instalação: cada pessoa aparece como "Participante 1", "Participante 2"…

## Roteiro (cerca de 10 minutos por pessoa)

Peça para a pessoa usar o assistente sozinha (`python assistente.py`) e observe sem ajudar.

| Situação | Tarefa pedida | O que observar |
|---|---|---|
| S1 | "Descubra o que mais gasta energia numa casa." (opção 1) | Entendeu a tabela? Soube dizer que é o chuveiro? |
| S2 | "Simule com o consumo da sua última conta." (opção 2) | Achou o kWh na conta? Entendeu as perguntas? Digitou algo inválido? |
| S3 | "Olhando o resultado, o que você faria primeiro?" | Entendeu a recomendação? Percebeu que é estimativa? |
| S4 | "Pergunte se vale a pena colocar placa solar." (opção 4) | A resposta ficou clara? Notou as fontes? |
| S5 | "Calcule quanto gasta um aparelho da sua casa." (opção 3) | Soube achar a potência (W) na etiqueta? |

Perguntas finais: (1) De 1 a 5, quanto ficou fácil de entender? (2) De 1 a 5, quanto isso ajudaria a decidir algo na sua casa? (3) Que palavra ou número você não entendeu? (4) O que faltou?

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

### Participante 2 — ____/____/2026

_A preencher._

### Participante 3 — ____/____/2026

_A preencher._

## Ajustes realizados

| Problema observado | Quem relatou | Ajuste feito | Arquivo |
|---|---|---|---|
| Não conseguia sair da tela de perguntas: digitou "0" e "fechar" e o assistente não entendeu | Participante 1 | Passou a aceitar "0", "sair", "voltar", "fechar" e Enter vazio; aviso na tela explicando como voltar; "sair" e "fechar" também funcionam no menu principal | `assistente.py` |
| O assistente só entendia perguntas com palavras-chave específicas | Participante 1 | (1) Lista de 11 temas numerados exibida na tela de perguntas: o usuário pode digitar só o número; (2) mais sinônimos e frases do dia a dia ("minha conta tá muito cara", "o que gasta mais", "quero gerar minha própria energia", "por que a conta não zera"); (3) quando não entende, mostra a lista de temas em vez de só uma mensagem de erro; (4) novo teste automático com essas frases | `energia/respostas.py`, `assistente.py`, `tests/test_calculos.py` |

## Verificações automáticas (não substituem o teste com pessoas)

`python -m unittest discover -s tests -v` — 20 testes: fórmulas de consumo, tarifa conferida com a fonte (R$ 0,9543/kWh a 200 kWh), faixas de ICMS, balanço de energia do solar, coerência da comparação, respostas com fonte, tratamento de entradas inválidas e reconhecimento de perguntas escritas com palavras do dia a dia (incluído após o teste com o Participante 1).
