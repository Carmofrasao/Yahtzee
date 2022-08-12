#!/usr/bin/python 
import ring_logic
import socket
import json

RECEBE_DE = 7003
ENVIA_PRA = 7000

# estrutura relativa ao jogador 1
jogador = {
    'numero' : 0,
    'bastao' : 1, 
    'jogada' : '',
    'aposta' : 0,
    'fichas' : 10,
    'sec'    : 1,
}

# ************************* JOGADA INICIA PELO JOGADOR 1 **************************
def init_partida():
    # jogador um define qual jogada ele quer fazer 
    jogador['jogada'] = input("Informe sua jogada: ") 
    jogador['jogada'] = jogador['jogada'].upper()
    jogador['aposta'] = 1

    mensage = {
        'jogador'   : jogador['numero'],
        'aposta'    : jogador['aposta'],
        'resultado' : 0,
        'fichas'    : 0,
        'ganhador'  : 0, 
        'contador'  : 1,
        'cont_resul': 1,
        'troca'     : 0,
        'exit'      : 0,
    }

    if jogador['jogada'] == '1 PAR':
        mensage['jogada'] = 0
    elif jogador['jogada'] == '1 TRIO':
        mensage['jogada'] = 1
    elif jogador['jogada'] == '2 PARES':
        mensage['jogada'] = 2
    elif jogador['jogada'] == '1 FULL HOUSE':
        mensage['jogada'] = 3
    elif jogador['jogada'] == '1 SEQUENCIA BAIXA':
        mensage['jogada'] = 4
    elif jogador['jogada'] == '1 SEQUENCIA ALTA':
        mensage['jogada'] = 5
    elif jogador['jogada'] == '1 QUADRA':
        mensage['jogada'] = 6
    elif jogador['jogada'] == '1 QUINTETO':
        mensage['jogada'] = 7

    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
    send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((ring_logic.LOCAL_HOST,ENVIA_PRA))) 

        
if __name__ == "__main__":
    print('O JOGO COMEÇOU!')
    init_partida()
    ring_logic.run_player(jogador, RECEBE_DE, ENVIA_PRA)

