# trab3-redes
Trabalho 3 da materia de rede 1 da Universidade Federal do Paraná
Feito por Anderson Frasão e Eduardo Gobbo.

Objetivo
Implementar o jogo desenvolvido em aula (uma variante do Yahtzee) com uma estrutura
de comunicação em Rede em Anel com passagem de bastão.

Execução
Devido ao uso de variáveis que necessitam menos de 8 bits para sua representação, foi utilizada uma biblioteca em python para manipular valores com n bits nos campos do pacote da mensagem. Para instalar este pacote, basta ter instalada a última versão de pip, e digitar
>pip install bitstring
Com a biblioteca instalada, basta executar 
> python pcx.py
Onde x representa o número da máquina de cada jogador, ou seja, inteiros de 1 a 4.
