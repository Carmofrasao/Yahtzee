#!/usr/bin/python

import socket 
# colocar o ip do pc aqui
# ip = input('digite o ip de conexao: ') 
ip = '192.168.0.108' 
port = 7001
addr = ((ip,port)) 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client_socket.connect(addr) 
mensagem = input("digite uma mensagem para enviar ao servidor") 
client_socket.send(mensagem.encode()) 
print('mensagem enviada') 
client_socket.close()