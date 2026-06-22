import socket
import time
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import faker
import random
import pygame

engine = create_engine("postgresql+psycopg2://postgres:228228765@localhost/PYTHON")
Base = declarative_base()

class Players(Base):
    __tablename__ = 'Players'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    adres = Column(String)
    x = Column(Integer, default=500)
    y = Column(Integer, default=500)
    size = Column(Integer, default=10)
    errors = Column(Integer, default=0)
    ABSspeed = Column(Integer, default=1)
    speedx = Column(Integer, default=0)
    speedy = Column(Integer, default=0)
    color = Column(String,default="red")
    w_wision = Column(Integer,default=800)
    h_wision = Column(Integer,default=600)


    def __init__(self, name, adres):
        self.name = name
        self.adres = adres

class LocalPlayer():
    def __init__(self, id, name, sock, adres):
        self.id = id
        self.name = name
        self.sock = sock
        self.adres = adres
        self.DB = s.get(Players, self.id)
        self.x = 500
        self.y = 500
        self.size = 10
        self.errors = 0
        self.ABSspeed = 1
        self.speedx = 0
        self.speedy = 0
        self.color="red"
        self.w_wision=800
        self.h_wision=600

    def syns(self):
        self.DB.x = self.x
        self.DB.y = self.y
        self.DB.size = self.size
        self.DB.errors = self.errors
        self.DB.ABSspeed = self.ABSspeed
        self.DB.speedx = self.speedx
        self.DB.speedy = self.speedy
        self.DB.color = self.color
        self.DB.w_wision = self.w_wision
        self.DB.h_wision = self.h_wision

        s.merge(self.DB)
        s.commit()

    def load(self):
        self.x = self.DB.x
        self.y = self.DB.y
        self.size = self.DB.size
        self.errors = self.DB.errors
        self.ABSspeed = self.DB.ABSspeed
        self.speedx =  self.DB.speedx
        self.speedy = self.DB.speedy
        self.color = self.DB.color
        self.w_wision = self.DB.w_wision
        self.h_wision = self.DB.h_wision 
        return self
    
    

    def update(self):
        if self.x - self.size<=0:
            if self.speedx>0:
                self.x += self.speedx
        elif self.x + self.size>=width_room:
            if self.speedx<0:
                self.x += self.speedx
        else:
            self.x += self.speedx

        if self.y - self.size<=0:
            if self.speedy>0:
                self.y += self.speedy
        elif self.y + self.size>=height_room:
            if self.speedy<0:
                self.y += self.speedy
        else:
            self.y += self.speedy

    def change_speed(self, vector):
        vector = find(vector)

        if vector[0] == 0 and vector[1] == 0:
            self.speedx = 0
            self.speedy = 0
        else:
            vector = vector[0] * self.ABSspeed, vector[1] * self.ABSspeed
            self.speedx = float(vector[0])
            self.speedy = float(vector[1])


def find(vector):
    start = vector.find('<')
    end = vector.find('>')
    if start < end and start != -1:
        data = vector[start + 1:end]
        data = data.split(',')
        data = list(map(float, data))
        return data
    return ''

def find_login(data):
    start = data.find('<')
    end = data.find('>')
    if start < end and start != -1:
        data = data[start + 1:end]
        data = data.split(',')
        return data
    return ''


Base.metadata.create_all(engine)
Session = sessionmaker(engine)
s = Session()

pygame.init()
width_room = 5000
height_room = 5000
width_server = 500
height_server = 500
screen = pygame.display.set_mode((width_server, height_server))
pygame.display.set_caption("SERVER")
clok = pygame.time.Clock()
Fps = 180

colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown'
          ,'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow'
          ,'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'SpringGreen', 'MediumSpringGreen', 'Turquoise'
          ,'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'DeepSkyBlue'
          ,'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue']

mob_count = random.randint(20,30)
fake = faker.Faker("ru_RU")



main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind(('localhost', 10000))
main_socket.setblocking(False)
main_socket.listen(5)
print('socket создан')
players = {}
run = True

for x in range(mob_count):
    server_mob = Players(fake.user_name(),None)
    server_mob.color=random.choice(colors)
    server_mob.x = random.randint(0,width_room)
    server_mob.y = random.randint(0,height_room)
    server_mob.speedx = random.uniform(-1,1)
    server_mob.speedy = random.uniform(-1,1)
    server_mob.size = random.randint(5,50)

    s.add(server_mob)
    s.commit()
    local_mob = LocalPlayer(server_mob.id,server_mob.name,None,None).load()
    players[server_mob.id] = local_mob
while run:
    clok.tick(Fps)
    try:
        new_socket, addr = main_socket.accept()
        print('Подключился', addr)
        new_socket.setblocking(False)
        login = new_socket.recv(1024).decode()
        addr_str = f'({addr[0]},{addr[1]})'
        player_db = Players(name=f'Player_{len(players) + 1}', adres=addr_str)
        if login.startswith('color'):
            data = find_login (login)
            player_db.name=data[0]
            player_db.color=data[1]
        s.add(player_db)
        s.commit()
        local_player = LocalPlayer(player_db.id, player_db.name, new_socket, addr_str).load()
        local_player.DB = player_db
        players[player_db.id] = local_player
    except BlockingIOError:
        pass

    for player_id in list(players.keys()):
        if players[player_id].sock is not None:
                
            try:
                data = players[player_id].sock.recv(1024).decode()
                if data:
                    print(data)
                    players[player_id].change_speed(data)
            except (BlockingIOError, ConnectionResetError, OSError):
                pass

    visable_bacteries={}
    for id in list(players):
        visable_bacteries[id]=[]
    pairs = list(players.items())
    for i in range(0,len(pairs)):
        for j in range(i+1,len(pairs)):
            hero1:LocalPlayer = pairs[i][1]
            hero2:LocalPlayer = pairs[j][1]
            dist_x = hero2.x - hero1.x
            dist_y = hero2.y - hero1.y
            if abs(dist_x)<=hero1.w_wision//2+hero2.size and abs(dist_y)<=hero1.h_wision//2+hero2.size:
                if hero1.adres is not None:
                    x = str(round(dist_x))
                    y = str(round(dist_y))
                    size = str(round(hero2.size))
                    color = hero2.color
                    data = f'{x} {y} {size} {color}'
                    visable_bacteries[hero1.id].append(data)
            if abs(dist_x)<=hero2.w_wision//2+hero1.size and abs(dist_y)<=hero2.h_wision//2+hero1.size:
                if hero2.adres is not None:
                    x = str(round(-dist_x))
                    y = str(round(-dist_y))
                    size = str(round(hero1.size))
                    color = hero1.color
                    data = f'{x} {y} {size} {color}'
                    visable_bacteries[hero2.id].append(data)    
    for id in list(players):
        visable_bacteries[id] = f'<{",".join(visable_bacteries[id])}>'


    for player_id in list(players.keys()):
        if players[player_id].sock is not None:
            try:
                players[player_id].sock.send(visable_bacteries[player_id].encode())
            except (ConnectionResetError, OSError):
                players[player_id].sock.close()
                s.query(Players).filter(Players.id == player_id).delete()
                s.commit()
                del players[player_id]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill('darkgreen')
    for player_id in players:
        player = players[player_id]
        x = player.x * width_server // width_room
        y = player.y * width_server // width_room
        size = player.size * width_server // width_room
        pygame.draw.circle(screen, player.color, (x, y), size)

    for player_id in list(players.keys()):
        players[player_id].update()
        players[player_id].syns()

    pygame.display.update()

s.close()
main_socket.close()
