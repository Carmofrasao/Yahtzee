#!/usr/bin/python 
import ring_logic
import socket
import json

RECEBE_DE = 7003
ENVIA_PRA = 7000

# estrutura relativa ao jogador 1
jogador = {
    'numero' : '1',
    'bastao' : 1, 
    'jogada' : '',
    'aposta' : 0,
    'fichas' : 6,
    'sec'    : 1,
}

# ************************* JOGADA INICIA PELO JOGADOR 1 **************************
def init_partida():
    # jogador um define qual jogada ele quer fazer 
    jogador['jogada'] = input("Informe sua jogada: ") 
    jogador['aposta'] = 1

    mensage = {
        'jogador'   : jogador['numero'],
        'jogada'    : jogador['jogada'],
        'aposta'    : jogador['aposta'],
        'resultado' : 0,
        'ganhador'  : '', 
        'contador'  : 1,
        'cont_resul': 1,
        'troca'     : 0,
        'exit'      : 0,
    }

    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
    send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((ring_logic.LOCAL_HOST,ENVIA_PRA))) 

        
if __name__ == "__main__":
    print('O JOGO COMEÇOU!')
    init_partida()
    ring_logic.run_player(jogador, RECEBE_DE, ENVIA_PRA)

