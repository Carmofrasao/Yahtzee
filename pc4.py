#!/usr/bin/python 

import socket 
import json

jogador = {
    'numero' : '4',
    'bastao' : 0, 
    'jogada' : '',
    'aposta' : '',
    'fichas' : 6,
    'sec'    : 1,
}

while True:
    # Criar um soquete UDP
    # Observe o uso de SOCK_DGRAM para pacotes UDP
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    # Atribuir endereço IP e número de porta ao soquete
    serv_socket.bind(('', 7002)) 

    print("aguardando jogada do jogador 3") 

    # Recebendo o pacote do cliente junto com o endereço de onde ele está vindo
    mensage, address = serv_socket.recvfrom(1024)

    # DESCONVERTENDO BYTES PARA DICIONARIO
    mensage = json.loads(mensage.decode('utf-8'))

    print('O jogador ' + mensage['jogador'] + ' jogou ' + mensage['jogada'] + ', apostando ' + mensage['aposta'] + ' ficha(s)')



    # Criar um soquete UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    cobrir = input("Deseja cobrir? (S/N) ")
    if cobrir == 'S':
        jogador['aposta'] = input("Informe quantas fichas deseja apostar: ")

        mensage = {
            'jogador' : jogador['numero'],
            'jogada'  : mensage['jogada'],
            'aposta'  : jogador['aposta'],
        }

    addr = (('192.168.0.108',7003))

    # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
    client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 