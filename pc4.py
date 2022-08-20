#!/usr/bin/python 
import ring_logic

RECEBE_DE = 7002
ENVIA_PRA = 7003

# estrutura relativa ao jogador 4
jogador = {
    'numero' : 3,
    'bastao' : 0, 
    'jogada' : '',
    'aposta' : 0,
    'fichas' : 6,
    'sec'    : 1,
}


if __name__ == "__main__":
    print('O JOGO COMEÇOU!')
    print('Aguarde sua vez!')
    print()
    ring_logic.run_player(jogador, RECEBE_DE, ENVIA_PRA)

    