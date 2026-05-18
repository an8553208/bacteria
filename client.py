import socket
import random
import pygame
import math
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

name = ''
color = ''

colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown'
          ,'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow'
          ,'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'SpringGreen', 'MediumSpringGreen', 'Turquoise'
          ,'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'DeepSkyBlue'
          ,'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue']

root = tk.Tk()
root.geometry('300x200')
root.title('login')



main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.connect(('localhost', 10000))
pygame.init()
width = 800
height = 600
CC = (width // 2, height // 2)
old = (0, 0)
radius = 10
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('бактерия')
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        vector = (pos[0] - CC[0], pos[1] - CC[1])
        lenv = math.sqrt(vector[0]**2 + vector[1]**2)
        if lenv != 0:
            vector = (vector[0] / lenv, vector[1] / lenv)
        if lenv < radius:
            vector = (0, 0)
        if vector != old:
            old = vector
            msg = f"<{vector[0]},{vector[1]}>"
            main_socket.send(msg.encode())

    try:
        main_socket.settimeout(0.1)
        data = main_socket.recv(1024).decode()
        if data:
            print(data)
    except socket.timeout:
        pass
    except ConnectionResetError:
        run = False
    except Exception:
        run = False

    screen.fill('darkgreen')
    pygame.draw.circle(screen, (255, 0, 0), CC, radius)
    pygame.display.update()

main_socket.close()
pygame.quit()
