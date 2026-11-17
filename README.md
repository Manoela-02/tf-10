# Projeto MiniGit

Este projeto implementa uma simulação simplificada do funcionamento interno do Git utilizando estruturas de dados fundamentais em Python (dicionários, listas, tuplas e filas), com contagem rigorosa de passos para análise de complexidade entre operações de leitura e escrita.

## Tabela de Medição

| commits | passos do commitar | passos do log |
| :--- | :--- | :--- |
| 10 | 2 | 10 |
| 100 | 2 | 100 |
| 1000 | 2 | 1000 |

## Questões Teóricas

1. **Por que o commitar gasta sempre 2 passos, e o log gasta mais conforme o histórico cresce?**
   O método de escrita `commitar` executa uma quantidade fixa de operações independentes do tamanho do histórico (criar o commit e atualizar o ponteiro da branch), resultando em custo constante. Em contrapartida, o método de leitura `log` precisa percorrer e visitar cada commit alcançável a partir do ponteiro atual, fazendo o número de passos escalar linearmente com a quantidade de nós visitados.

2. **Por que mensagem(commit) gasta 1 passo e buscar(texto) pode gastar muitos?**
   A consulta de `mensagem` utiliza uma chave exata em um dicionário, o que permite acesso direto em tempo constante de 1 passo. Já o método `buscar` procura por conteúdo dentro das mensagens, precisando iterar sequencialmente pelos commits gerados até encontrar a correspondência ou esgotar a busca.

3. **Por que o merge é um commit com dois pais, e por que isso faz do histórico um grafo, e não uma lista?**
   O merge une duas linhas de desenvolvimento independentes, recolhendo os ponteiros das duas branches envolvidas como ascendentes diretos (pais). Essa capacidade de possuir múltiplos graus de conexão faz com que o histórico deixe de ser uma estrutura linear simples e passe a comportar-se como um grafo direcionado acíclico (DAG).

4. **Por que o método pais devolve uma tupla, e não a lista que está guardada dentro do dicionário?**
   Retornar uma tupla (imutável) impede que códigos externos manipulem ou corrompam a estrutura interna de referências dos pais de um commit armazenada no dicionário privado da classe, preservando a integridade do histórico.