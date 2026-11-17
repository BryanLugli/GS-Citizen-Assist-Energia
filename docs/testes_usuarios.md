# Testes com usuários

> **Este arquivo deve ser preenchido pelo grupo com testes reais.** O roteiro e as tabelas já estão prontos; os resultados não foram inventados. Teste com 3 a 5 pessoas do público (familiares, vizinhos, colegas que pagam conta de luz). Não anote nome, endereço nem número da instalação — use "Participante 1", "Participante 2"…

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

Data(s): ____/____/2026 — Versão testada (commit): ________

| Participante | Perfil (sem dados pessoais) | Situações | Clareza (1–5) | Utilidade (1–5) | Comentários |
|---|---|---|---|---|---|
| P1 | ex.: adulto, mora em casa própria | S1–S5 | | | |
| P2 | | | | | |
| P3 | | | | | |

## Ajustes realizados

| Problema observado | Quem relatou | Ajuste feito | Arquivo/commit |
|---|---|---|---|
| | | | |

## Verificações automáticas (não substituem o teste com pessoas)

`python -m unittest discover -s tests -v` — 19 testes: fórmulas de consumo, tarifa conferida com a fonte (R$ 0,9543/kWh a 200 kWh), faixas de ICMS, balanço de energia do solar, coerência da comparação, respostas com fonte e tratamento de entradas inválidas.
