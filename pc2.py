#!/usr/bin/python 

import socket 

# Criar um soquete UDP
# Observe o uso de SOCK_DGRAM para pacotes UDP
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Atribuir endereço IP e número de porta ao soquete
serv_socket.bind(('', 7000)) 

print("aguardando mensagem") 

# Recebendo o pacote do cliente junto com o endereço de onde ele está vindo
message, address = serv_socket.recvfrom(1024)

print("mensagem recebida: "+ message.decode())



# Criar um soquete UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

mensagem = input("digite uma mensagem para enviar ao servidor") 

addr = (('192.168.0.108',7001))

client_socket.sendto(mensagem.encode(), addr) 

print('mensagem enviada') 