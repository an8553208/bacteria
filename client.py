import socket
import random
import pygame
main_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
main_socket.connect(('localhost',10000))
while True:
    main_socket.send(f'{random.randint(1,9)}'.encode())
