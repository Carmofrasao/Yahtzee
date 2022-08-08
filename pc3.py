#!/usr/bin/python 

import socket 
import json

ip = '192.168.0.108'

# estrutura relativa ao jogador 3
jogador = {
    'numero' : '3',
    'bastao' : 0, 
    'jogada' : '',
    'aposta' : 0,
    'fichas' : 6,
    'sec'    : 1,
}

while True:
    # Criar um soquete UDP
    # Observe o uso de SOCK_DGRAM para pacotes UDP
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    # Atribuir endereço IP e número de porta ao soquete
    serv_socket.bind(('', 7001))  

    # Recebendo o pacote do cliente junto com o endereço de onde ele está vindo
    mensage, address = serv_socket.recvfrom(1024)

    # DESCONVERTENDO BYTES PARA DICIONARIO
    mensage = json.loads(mensage.decode('utf-8'))

    if mensage['contador'] != 0:
        # caso ainda esteja recolhendo as jogadas

        print('O jogador ' + mensage['jogador'] + ' jogou ' + mensage['jogada'] + ', apostando ' + str(mensage['aposta']) + ' ficha(s)')

        if mensage['contador'] < 4:
            # caso nao tenha passado por todos os jogadores recolhendo suas jogadas
            mensage['contador'] += 1

            # Criar um soquete UDP
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

            cobrir = input("Deseja cobrir? (S/N) ")
            if cobrir == 'S':
                # verifica se o jogador atual deseja cobrir a aposta dos jogadores anteriores

                jogador['aposta'] = mensage['aposta'] + 1
                # cobre a aposta e manda pro proximo jogador
                mensage = {
                    'jogador' : jogador['numero'],
                    'jogada'  : mensage['jogada'],
                    'aposta'  : jogador['aposta'],
                    'contador': mensage['contador'],
                }

            addr = ((ip,7002))

            # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
            client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 
        else:
            # caso tenha dado a volta
            if jogador['aposta'] == mensage['aposta']:
                # verifica se o jogador atual é quem vai fazer a jogada
                print('O jogador ' + jogador['numero'] + ' vai jogar')
                # AQUI DEVE SER FEITO O ROLE DAS JOGADAS
                mensage['contador'] = 0
                addr = ((ip,7002))

                # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
                client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 
            else:
                print('A jogada deve ser passada para o jogador que apostou '+ str(mensage['aposta']))
                addr = ((ip,7002))

                # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
                client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 
    else:
        # apos a jogada ser efetuada
        if jogador['bastao'] == 1:
            # se encontrou o jogador com o bastao, manda pro proximo
            jogador['bastao'] = 0
            addr = ((ip,7002))

            # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
            client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 
        else: 
            # AQUI ESTA ERRADO, ELE PEGA O PROXIMO QUE ESTA COM jogador['bastao'] == 0
            # O CERTO É PEGAR O PROXIMO DEPOIS DO QUE ESTA COM jogador['bastao'] == 1
            
            # proximo jogador a jogar
            jogador['bastao'] = 1
            # Criar um soquete UDP
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

            # O proximo jogador defini qual jogada ele quer fazer
            jogador['jogada'] = input("Informe sua jogada: ") 
            jogador['aposta'] = 1

            mensage = {
                'jogador' : jogador['numero'],
                'jogada'  : jogador['jogada'],
                'aposta'  : jogador['aposta'],
                'contador': 1,
            }

            addr = ((ip,7002))

            # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
            client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 