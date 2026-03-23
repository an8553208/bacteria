import socket
import random
import pygame
main_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
main_socket.connect(('localhost',10000))
pygame.init()
width = 800
height = 600
CC = (width//2,height//2)
old = (0,0)
radius = 50
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('бактерия')
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        vector = (pos[0]-CC[0],pos[1]-CC[1])
        if old != vector:
            old = vector
            msg = ('')
    main_socket.send(f'{random.randint(1,9)}'.encode())
    data = main_socket.recv(1024).decode()
    print (data)

