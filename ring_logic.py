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

def par(dados):
    for i in range(1, 7):
        if dados.count(i) >= 2:
            return 1
    return 0

def trio(dados):
    for i in range(1, 7):
        if dados.count(i) >= 3:
            return 1
    return 0

def pares(dados):
    p_i = 0
    for i in range(1, 7):
        if dados.count(i) >= 2:
            p_i = i
            break
    for i in range(1, 7):
        if dados.count(i) >= 2 and i != p_i:
            return 1
    return 0

def full(dados):
    p_i = 0
    for i in range(1, 7):
        if dados.count(i) >= 2:
            p_i = i
            break
    for i in range(1, 7):
        if dados.count(i) >= 3 and i != p_i:
            return 1
    return 0

def seq_b(dados):
    dados.sort()
    if dados[0] == 1:
        for i in range(1, 5):
            if dados[i] != i+1:
                return 0
        return 1
    else:
        return 0

def seq_a(dados):
    dados.sort()
    if dados[0] == 2:
        for i in range(1, 5):
            print(dados[i])
            if dados[i] != i+1:
                return 0
        return 1
    else:
        return 0

def quadra(dados):
    for i in range(1, 7):
        if dados.count(i) >= 4:
            return 1
    return 0

def quinteto(dados):
    for i in range(1, 7):
        if dados.count(i) >= 5:
            return 1
    return 0

def jogada(jogada):
    arr = list()
    for i in range(0, 5):
        arr.append(random.randint(1, 6))
    
    for i in range(2):
        print('Rodada '+str(i+1))
        print(arr)
        print()
        inp = list(map(int, input("Quais dados deseja jogar novamente: ").split()))
        print()
        for i in inp:
            arr[i-1] = random.randint(1, 6)
    print('Rodada 3')
    print(arr)
    print()

    if jogada == '1 PAR':
        return par(arr)
    elif jogada == '1 TRIO':
        return trio(arr)
    elif jogada == '2 PARES':
        return pares(arr)
    elif jogada == '1 FULL HOUSE':
        return full(arr)
    elif jogada == '1 SEQUENCIA BAIXA':
        return seq_b(arr)
    elif jogada == '1 SEQUENCIA ALTA':
        return seq_a(arr)
    elif jogada == '1 QUADRA':
        return quadra(arr)
    elif jogada == '1 QUINTETO':
        return quinteto(arr)
    
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
                print('O jogador '+ mensage['ganhador'] + ' ganhou a aposta, ficando com '+str(mensage['fichas'])+' fichas')
            else:
                print('O jogador '+ mensage['ganhador'] + ' perdeu a aposta, ficando com '+str(mensage['fichas'])+' fichas')
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
                cobrir = cobrir.upper()
                if cobrir == 'S':
                    # verifica se o jogador atual deseja cobrir a aposta dos jogadores anteriores

                    jogador['aposta'] = mensage['aposta'] + 1
                    # cobre a aposta e manda pro proximo jogador
                    mensage = {
                        'jogador'   : jogador['numero'],
                        'jogada'    : mensage['jogada'],
                        'aposta'    : jogador['aposta'],
                        'contador'  : mensage['contador'],
                        'fichas'    : 0,
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
                    mensage['resultado'] = jogada(mensage['jogada'])
                    if(mensage['resultado'] == 1):
                        print('PARABENS, VOCÊ GANHOU!')
                        print()
                        jogador['fichas'] += fichas[mensage['jogada']]
                        mensage['fichas'] = jogador['fichas']
                        print('Seu saldo é de '+str(jogador['fichas'])+' fichas')
                        print()
                        if jogador['fichas'] <= 0:
                            print('Infelizmente você esta sem ficha!')
                            mensage['exit'] = 1
                            send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((LOCAL_HOST,send_port)))
                            exit()
                    else:
                        print('NÃO FOI DESSA VEZ, VOCÊ PERDEU')
                        print()
                        print('Seu saldo é de '+str(jogador['fichas'])+' fichas')
                        print()
                        mensage['fichas'] = jogador['fichas']
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
                jogador['jogada'] = jogador['jogada'].upper()
                jogador['aposta'] = 1

                mensage = {
                    'jogador'   : jogador['numero'],
                    'jogada'    : jogador['jogada'],
                    'aposta'    : jogador['aposta'],
                    'fichas'    : 0,
                    'resultado' : 0,
                    'ganhador'  : '', 
                    'contador'  : 1,
                    'cont_resul': 1,
                    'troca'     : 0,
                    'exit'      : 0,
                }

                # CONVERTENDO DICIONARIO PARA BYTES E MANDANDO A MENSAGEM PARA O PROXIMO
                send_sock.sendto(json.dumps(mensage,indent=2).encode('utf-8'), ((LOCAL_HOST,send_port))) 


    