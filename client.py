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

def scroll(event):
    global color
    color=combo.get()
    style.configure("TCombobox",fieldbackground=color,background="white")

def log ():
    global name
    name = row.get()
    if name and color:
        root.destroy()
        root.quit()
    else:
        tk.messagebox.showerror("ошибка","ты не ввёл имя или цвет")
def find(data):
    start = data.find('<')
    end = data.find('>')
    if start < end and start != -1:
        data = data[start + 1:end]
        data = data.split(',')
        return data
    return ''
def draw_bacteries(data):
    for bug in data:
        data_bug = bug.split(" ")
        x = CC[0] + int(data_bug[0])
        y = CC[1] + int(data_bug[1])
        size = int(data_bug[2])
        color = data_bug[3]
        pygame.draw.circle(screen, color, (x, y), size)




root = tk.Tk()
root.geometry('300x200')
root.title('login')
style = ttk.Style()
style.theme_use('clam')
namelabel = tk.Label(root,text='enter your name:')
namelabel.pack()
row= tk.Entry(root,width=30,justify="center")
row.pack()
colorlabel = tk.Label(root,text='choose your color:')
colorlabel.pack()
combo = ttk.Combobox(root,values = colors,textvariable=color)
combo.pack()
combo.bind('<<ComboboxSelected>>',scroll)
login = tk.Button(root,text='play game',command=log)
login.pack()


root.mainloop()


main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.connect(('localhost', 10000))
main_socket.send(f'color:<{name},{color}>'.encode())
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

    
    data = main_socket.recv(1024).decode()
    data = find(data)


    print (data)
    screen.fill('darkgreen')
    if data!=['']:
        radius = int(data[0])
        draw_bacteries(data[1:])
    pygame.draw.circle(screen,color, CC, radius)
    pygame.display.update()

main_socket.close()
pygame.quit()
