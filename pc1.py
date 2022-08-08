#!/usr/bin/python 

import socket
import json

jogador = {
    'numero' : '1',
    'bastao' : 1, 
    'jogada' : '',
    'aposta' : 0,
    'fichas' : 6,
    'sec'    : 1,
}

# JOGADA INICIA PELO JOGADOR 1 ***************************************************
# Criar um soquete UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

jogador['jogada'] = input("Informe sua jogada: ") 
jogador['aposta'] = 1

mensage = {
    'jogador' : jogador['numero'],
    'jogada'  : jogador['jogada'],
    'aposta'  : jogador['aposta'],
    'contador': 1,
}

addr = (('192.168.0.108',7000))

client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 

while True:
    # Criar um soquete UDP
    # Observe o uso de SOCK_DGRAM para pacotes UDP
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    # Atribuir endereço IP e número de porta ao soquete
    serv_socket.bind(('', 7003)) 

    print("aguardando jogada do jogador 4") 

    # Recebendo o pacote do cliente junto com o endereço de onde ele está vindo
    mensage, address = serv_socket.recvfrom(1024)

    # DESCONVERTENDO BYTES PARA DICIONARIO
    mensage = json.loads(mensage.decode('utf-8'))

    print('O jogador ' + mensage['jogador'] + ' jogou ' + mensage['jogada'] + ', apostando ' + str(mensage['aposta']) + ' ficha(s)')
    
    if mensage['contador'] < 4:
        
        mensage['contador'] += 1

        # Criar um soquete UDP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

        cobrir = input("Deseja cobrir? (S/N) ")
        if cobrir == 'S':
            jogador['aposta'] = mensage['aposta'] + 1

            mensage = {
                'jogador' : jogador['numero'],
                'jogada'  : mensage['jogada'],
                'aposta'  : jogador['aposta'],
                'contador': mensage['contador'],
            }

        addr = (('192.168.0.108',7000))

        # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
        client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 
    else:
        if jogador['aposta'] == mensage['aposta']:
            print('o jogador ' + jogador['numero'] + ' vai jogar')
        else:
            print('A jogada deve ser passada para o jogador que apostou '+ str(mensage['aposta']))