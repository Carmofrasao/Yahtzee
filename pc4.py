#!/usr/bin/python 

import socket 
host = '' 
port = 7003
addr = (host, port) 
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
serv_socket.bind(addr) 
serv_socket.listen(10) 
print('aguardando conexao') 
con, cliente = serv_socket.accept() 
print('conectado')
print("aguardando mensagem") 
recebe = con.recv(1024) 
print("mensagem recebida: "+ recebe.decode())
serv_socket.close()

ip = '192.168.0.108' 
port = 7003
addr = ((ip,port)) 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client_socket.connect(addr) 
mensagem = input("digite uma mensagem para enviar ao servidor") 
client_socket.send(mensagem.encode()) 
print('mensagem enviada') 
client_socket.close()