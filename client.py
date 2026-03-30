import socket
import random
import pygame
import math
main_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
main_socket.connect(('localhost',10000))
pygame.init()
radius = 50
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
        lenv = math.sqrt(vector[0]**2 + vector[1]**2)
        vector = (vector[0]/lenv,vector[1]/lenv)
        if lenv < radius:
            vector = (0,0)
        if vector != old:
            old = vector
            msg = f"<{vector[0]},{vector[1]}>"
            main_socket.send(msg.encode())
    data = main_socket.recv(1024).decode()
    print (data)
    screen.fill('green')
    pygame.draw.circle(screen, (255, 0, 0), CC, radius)
    pygame.display.update()

