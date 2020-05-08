# Jogo de Damas com Inteligência Artificial

Este projeto foi desenvolvido em 2019-1, para a cadeira de Inteligência Artificial do bacharelado de Ciência da Computação na Universidade Federal Fluminense (UFF). Alguns projetos foram sugeridos e o grupo optou por construir um **Jogo de Damas**, implementando duas técnicas de busca como agentes.

O grupo é composto por 4 alunos: [Bruno Paiva](https://github.com/brunopaivasantos), [Marcos Dos Reis](https://github.com/reismarcos), [Rafael Duarte](https://github.com/rafaeldcampbell) e [Raphael Guizan](https://github.com/Raphaguizan).

### Regras
O jogo conta com um tabuleiro de 64 casas (alternando escuras e claras) e 24 peças (12 brancas e 12 pretas). Os jogadores se posicionam de frente e organizam as peças nas casas escuras das três primeiras fileiras, orientando o tabuleiro de modo que a primeira casa à esquerda seja escura. As peças brancas começam, sempre se movimentando na diagonal e para frente, ocupando uma casa vazia que seja diretamente vizinha; caso uma das diagonais vizinhas esteja ocupada por uma peça oponente e a diagonal seguinte esteja livre, o jogador deve capturá-la, ocupando a casa seguinte e jogando novamente.
Caso alcance a fileira mais próxima do oponente, a peça passa a ser uma *dama*, representada por uma peça dupla. As damas podem se movimentar quantas casas desejarem, tanto nas diagonais para frente quanto para trás; a *dama* não pode pular peças de sua cor, podendo pular somente uma única peça oponente, capturando-a. O jogo termina quando alguém consegue capturar todas as peças do oponente, vencendo a partida, ou quando há empate.

### Tabuleiro e peças
O objetivo do projeto é manter um visual simplificado e utilizar linhas de comando para realizar toda a interação. Para representar as casas vazias, usa-se \"**.**\" para escuras e \"**-**\" para claras, em uma disposição matricial. As peças simples serão representadas por consoantes minúsculas, sendo \"**w**\" para brancas e \"**b**\" para pretas; as duplas (ou damas) são representadas por maiúsculas. O tabuleiro é exibido para o usuário sempre no estado atual, com a numeração de linhas e colunas que vai de 0 a 7.

~~~
7    w  -  w  -  w  -  w  -
6    -  w  -  w  -  w  -  w
5    w  -  w  -  w  -  w  -
4    -  .  -  .  -  .  -  .
3    .  -  .  -  .  -  .  -
2    -  b  -  b  -  b  -  b
1    b  -  b  -  b  -  b  -
0    -  b  -  b  -  b  -  b

     0  1  2  3  4  5  6  7  
~~~

### Agentes
Ao iniciar o jogo, o usuário deve informar quem será o jogador a controlar as peças brancas; em seguida, informa um jogar para as pretas. As opções de agentes são:
- IA Minimax com Poda Alfa e Beta
- IA Minimax com profundidade limitada e avaliação heuristica
- Você

### Como jogar
Escolhidos os agentes, o tabuleiro será exibido e as peças brancas devem começar. Todos os movimentos são descritos de forma matricial, em pares **\<linha\> \<coluna\>**, indicando origem e destino. Caso seja a vez de um jogador real, o sistema perguntará qual peça deseja mover e para onde deseja movê-la.

> Qual peça você quer mover? \<linha\> \<coluna\>
 
> Para onde você quer ir? \<linha\> \<coluna\>

A tela é atualizada a cada jogada, exibindo o tabuleiro atualizado. Exibe-se, ainda, uma linha com informações da última jogada, com o número, o jogador, o movimento e os eventos consequentes.

> Jogada 2 B ==>  (2, 1) -> (3, 0) |  capturando 0 peça(s)

> Jogada 58 W ==>  (5, 4) -> (7, 6) |  capturando 1 peça(s) e virando dama

*Obs. A tela é limpa a cada jogada, exibindo o estado atual e o último movimento. A tela exibida fica congelada, a cada jogada, durante **1 segundo**. 

Ao final de cada rodada, exibe-se o ganhador e o usuário deve informar se deseja jogar outra rodada com os mesmos agentes.

~~~
=========== Brancas ganharam =============
Deseja continuar jogando? (s/n)
~~~

### Log
Alguns arquivos de *log* são gerados automaticamente, tanto para cada jogo quanto para cada rodada de um mesmo jogo. O sistema gera dois tipos de *logs*:

- **Log geral**: 
Guarda os agentes escolhidos, quem ganhou cada rodada e em quanto tempo (desconsiderando os segundos onde a tela fica congelada).
~~~
Blacks: Heuristic
Whites: Pruning

Para o jogo 1 ==> brancas vencem em 5.978464126586914 segundos

Para o jogo 2 ==> brancas vencem em 2.9313442707061768 segundos
~~~
> Log\_for\_whole\_play\_black\_(black player)\_vs\_white\_(white player)\_(ano)\_(mes)\_(dia)\_(hora)\_(minuto)\_(segundo).txt


- **Log do jogador**: Para cada jogador e cada rodada, é gerado um arquivo que guarda, jogada a jogada, o tempo decorrido, número de nós visitados (0, caso não seja IA), número de nós podados (0, caso não seja IA com poda) e a jogada realizada. Ao fim, indica se foi uma vitória ou derrota.

~~~
Para a jogada 1 ==> 0.015579700469970703 segundos
Para a jogada 1 ==> visitados 32 nós, com 25 podados
Para a jogada 1 ==> (5, 2) -> (4, 3) |  capturando 0 peça(s)

Para a jogada 3 ==> 0.0 segundos
Para a jogada 3 ==> visitados 20 nós, com 13 podados
Para a jogada 3 ==> (6, 1) -> (5, 2) |  capturando 0 peça(s)

[...]

=========== VITÓRIA =============

~~~

> Log\_for\_(cor)\_(player)\_(ano)\_(mes)\_(dia)\_(hora)\_(minuto)\_(segundo).txt

*Obs. O repositório conta com exemplos de logs para algumas possibilidades de jogos. Os demais logs gerados durante a execução do código serão salvos dentro do diretório **log**.
  
### Mais informações
O repositório conta com um documento pdf, entregue como parte da avaliação, onde consta uma explicação mais detalhada das regras, características do ambiente e indicadores utilizados para a implementação dos algoritmos de busca.

### Como jogar
É necessário ter uma versão de [Python 3](https://www.python.org/downloads/) instalada. Para jogar, basta executar o arquivo **main.py**, que está no diretório **src**.

\*Obs. Se você adicionou o python às variáveis de ambiente e é usuário do Windows, basta clicar em **execute.cmd** que será executado o comando `python src/main.py` e o jogo abrirá no prompt de comando. *Pode ser necessário trocar `python` por outro nome, dependendo de como a variável foi salva.*