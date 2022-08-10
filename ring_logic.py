import socket
import json
import random

LOCAL_HOST = '127.0.0.1'

fichas = {
    '1 PAR'             : 2,
    '1 TRIO'            : 3,
    '2 PARES'           : 4,
    '1 FULL HOUSE'      : 5,
    '1 SEQUENCIA BAIXA' : 7,
    '1 SEQUENCIA ALTA'  : 7,
    '1 QUADRA'          : 10,
    '1 QUINTETO'        : 15, 
}

def jogar_novamente(n, atual):
    joga = input('Deseja jogar o dado '+str(n)+' novamente? (S/N) ')
    if joga == 'S':
        return random.randint(1, 6)
    else:
        return atual

def jogada():
    arr = list()
    for i in range(0, 5):
        arr.append(random.randint(1, 6))
    
    for i in range(2):
        print(f"o resultado da jogada é: {arr}")
        inp = list(map(int, input("mude os dados: ").split()))
        for i in inp:
            arr[i-1] = random.randint(1, 6)

    # AQUI DEVE SER FEITA A LOGICA PARA VERIFICAR SE O RESULTADO FINAL DOS DADOS É IGUAL A APOSTA FEITA

    return 0

def run_player(jogador, recv_port, send_port):
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    recv_sock.bind(('', recv_port))
    
    while True:
        # Recebendo o pacote do cliente junto com o endereço de onde ele está vindo
        mensage, address = recv_sock.recvfrom(1024)

        # DESCONVERTENDO BYTES PARA DICIONARIO
        mensage = json.loads(mensage.decode('utf-8'))
        if mensage['exit'] == 1:
            print()
            print('O jogo acabou, o jogador numero '+mensage['jogador']+' esta sem ficha!')
            send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((LOCAL_HOST,send_port)))
            exit()

        if(mensage['contador'] == 0 and mensage['cont_resul'] < 4 and mensage['ganhador'] != jogador['numero']):
            print()
            if mensage['resultado'] == 1:
                print('O jogador '+ mensage['ganhador'] + ' ganhou a aposta')
            else:
                print('O jogador '+ mensage['ganhador'] + ' perdeu a aposta')
            print()
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
                        'exit'      : 0,
                    }

                # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
                send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((LOCAL_HOST,send_port))) 
            else:
                # caso tenha dado a volta
                if jogador['aposta'] == mensage['aposta']:
                    # verifica se o jogador atual é quem vai fazer a jogada
                    print()
                    print('O jogador ' + jogador['numero'] + ' vai jogar')
                    print()
                    jogador['fichas'] -= jogador['aposta']
                    # AQUI DEVE SER FEITO O ROLE DAS JOGADAS
                    mensage['resultado'] = jogada()
                    if(mensage['resultado'] == 1):
                        print('PARABENS, VOCÊ GANHOU!')
                        jogador['fichas'] += fichas[mensage['jogada']]
                    else:
                        print('NÃO FOI DESSA VEZ, VOCÊ PERDEU')
                        jogador['fichas'] -= fichas[mensage['jogada']]
                        if jogador['fichas'] <= 0:
                            print('O jogo acabou, o jogador numero '+jogador['numero']+' esta sem ficha!')
                            mensage['exit'] = 1
                            send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((LOCAL_HOST,send_port)))
                            exit()
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
                    'exit'      : 0,
                }

                # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
                send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((LOCAL_HOST,send_port))) 


    