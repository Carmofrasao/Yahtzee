import socket
import json

LOCAL_HOST = '127.0.0.1'


def jogada():
    return 1


def run_player(jogador, recv_port, send_port):
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    recv_sock.bind(('', recv_port))
    
    while True:
        # Recebendo o pacote do cliente junto com o endereço de onde ele está vindo
        mensage, address = recv_sock.recvfrom(1024)

        # DESCONVERTENDO BYTES PARA DICIONARIO
        mensage = json.loads(mensage.decode('utf-8'))

        if(mensage['contador'] == 0 and mensage['cont_resul'] < 4 and mensage['ganhador'] != jogador['numero']):
            if mensage['resultado'] == 1:
                print('O jogador '+ mensage['ganhador'] + ' ganhou a aposta')
            else:
                print('O jogador '+ mensage['ganhador'] + ' perdeu a aposta')
            mensage['cont_resul'] += 1

            # passa pro proximo
            # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
            send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((LOCAL_HOST,send_port))) 

            continue


        if mensage['contador'] != 0:
            # caso ainda esteja recolhendo as jogadas
            
            if mensage['contador'] < 4:

                print('O jogador ' + mensage['jogador'] + ' jogou ' + mensage['jogada'] + ', apostando ' + str(mensage['aposta']) + ' ficha(s)')

                # caso nao tenha passado por todos os jogadores recolhendo suas jogadas
                mensage['contador'] += 1

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

                # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
                send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((LOCAL_HOST,send_port))) 
            else:
                # caso tenha dado a volta
                if jogador['aposta'] == mensage['aposta']:
                    # verifica se o jogador atual é quem vai fazer a jogada
                    print('O jogador ' + jogador['numero'] + ' vai jogar')
                    # AQUI DEVE SER FEITO O ROLE DAS JOGADAS
                    mensage['resultado'] = jogada()
                    if(mensage['resultado'] == 1):
                        print('PARABENS, VOCÊ GANHOU!')
                    else:
                        print('NÃO FOI DESSA VEZ, VOCÊ PERDEU')
                    mensage['contador'] = 0
                    mensage['ganhador'] = jogador['numero']

                    # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
                    send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((LOCAL_HOST,send_port))) 
                else:
                    # se não for o jogador, passa pro proximo
                    # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
                    send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((LOCAL_HOST,send_port))) 
        else:
            # apos a jogada ser efetuada
            if jogador['bastao'] == 1:
                mensage['troca'] = 1
                # se encontrou o jogador com o bastao, manda pro proximo
                jogador['bastao'] = 0

                # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
                send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((LOCAL_HOST,send_port))) 
            elif mensage['troca'] == 0:

                # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
                send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((LOCAL_HOST,send_port))) 
            else: 
                # proximo jogador a jogar
                jogador['bastao'] = 1

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

                # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
                send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((LOCAL_HOST,send_port))) 


    