#!/usr/bin/python 

import socket 

pc4 = {
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

    print(mensage.decode())



    # Criar um soquete UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    cobrir = input("Deseja cobrir? (S/N) ")
    if cobrir == 'S':
        pc4['aposta'] = input("Informe quantas fichas deseja apostar: ")

        mensage = 'O jogador 4 jogou ' + pc4['jogada'] + ', apostando ' + pc4['aposta'] + ' ficha(s)' 

        addr = (('192.168.0.108',7003))
        client_socket.sendto(mensage.encode(), addr) 

        continue

    addr = (('192.168.0.108',7003))
    client_socket.sendto(mensage, addr) 