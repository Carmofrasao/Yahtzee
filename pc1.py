#!/usr/bin/python 

import socket
import json

ip = '192.168.0.108'

# estrutura relativa ao jogador 1
jogador = {
    'numero' : '1',
    'bastao' : 1, 
    'jogada' : '',
    'aposta' : 0,
    'fichas' : 6,
    'sec'    : 1,
}

def jogada():
    return 1

# ************************* JOGADA INICIA PELO JOGADOR 1 **************************
# Criar um soquete UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

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
}

addr = ((ip,7000))

# CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 

while True:
    # Criar um soquete UDP
    # Observe o uso de SOCK_DGRAM para pacotes UDP
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    # Atribuir endereço IP e número de porta ao soquete
    serv_socket.bind(('', 7003)) 

    # Recebendo o pacote do cliente junto com o endereço de onde ele está vindo
    mensage, address = serv_socket.recvfrom(1024)

    # DESCONVERTENDO BYTES PARA DICIONARIO
    mensage = json.loads(mensage.decode('utf-8'))

    if(mensage['contador'] == 0 and mensage['cont_resul'] < 4 and mensage['ganhador'] != jogador['numero']):
        if mensage['resultado'] == 1:
            print('O jogador '+ mensage['ganhador'] + ' ganhou a aposta')
        else:
            print('O jogador '+ mensage['ganhador'] + ' perdeu a aposta')
        mensage['cont_resul'] += 1
        # se não for o jogador, passa pro proximo
        addr = ((ip,7000))

        # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
        client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 

        continue


    if mensage['contador'] != 0:
        # caso ainda esteja recolhendo as jogadas
        
        if mensage['contador'] < 4:

            print('O jogador ' + mensage['jogador'] + ' jogou ' + mensage['jogada'] + ', apostando ' + str(mensage['aposta']) + ' ficha(s)')

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
                    'jogador'   : jogador['numero'],
                    'jogada'    : mensage['jogada'],
                    'aposta'    : jogador['aposta'],
                    'contador'  : mensage['contador'],
                    'resultado' : 0,
                    'ganhador'  : '', 
                    'cont_resul': 1,
                    'troca'     : 0,
                }

            addr = ((ip,7000))

            # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
            client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 
        else:
            # caso tenha dado a volta
            if jogador['aposta'] == mensage['aposta']:
                # verifica se o jogador atual é quem vai fazer a jogada
                print('O jogador ' + jogador['numero'] + ' vai jogar')
                # AQUI DEVE SER FEITO O ROLE DAS JOGADAS
                mensage['resultado'] = jogada()
                mensage['contador'] = 0
                mensage['ganhador'] = jogador['numero']
                addr = ((ip,7000))

                # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
                client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 
            else:
                # se não for o jogador, passa pro proximo
                addr = ((ip,7000))

                # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
                client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 
    else:
        # apos a jogada ser efetuada
        if jogador['bastao'] == 1:
            mensage['troca'] = 1
            # se encontrou o jogador com o bastao, manda pro proximo
            jogador['bastao'] = 0
            addr = ((ip ,7000))

            # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
            client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 
        elif mensage['troca'] == 0:
            addr = ((ip ,7000))

            # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
            client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 
        else: 
            # proximo jogador a jogar
            jogador['bastao'] = 1
            # Criar um soquete UDP
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

            # O proximo jogador faz a jogada
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
            }

            addr = ((ip,7000))

            # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
            client_socket.sendto(json.dumps(mensage,indent=2).encode('utf-8'), addr) 