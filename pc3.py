#!/usr/bin/python 
import ring_logic
import socket 
import json

RECEBE_DE = 7001
ENVIA_PRA = 7002

# estrutura relativa ao jogador 3
jogador = {
    'numero' : 2,
    'bastao' : 0, 
    'jogada' : '',
    'aposta' : 0,
    'fichas' : 10,
    'sec'    : 1,
}


if __name__ == "__main__":
    print('O JOGO COMEÇOU!')
    print('Aguarde sua vez!')
    print()
    ring_logic.run_player(jogador, RECEBE_DE, ENVIA_PRA)

    