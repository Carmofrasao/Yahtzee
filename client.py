#!/usr/bin/python

import socket  

# Criar um soquete UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

mensagem = input("digite uma mensagem para enviar ao servidor") 

addr = (('192.168.0.108',7000))

client_socket.sendto(mensagem.encode(), addr) 

print('mensagem enviada') 