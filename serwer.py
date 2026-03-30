import socket
import time
import psycopg2
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker
import faker
import random




engine = create_engine("postgresql+psycopg2://postgres:228228765@localhost/PYTHON")
Base = declarative_base()
class Players(Base):
    __tablename__ = 'Players'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String)
    adres = Column(String)
    x = Column(Integer,default=500)
    y = Column(Integer,default=500)
    size = Column(Integer,default=50)
    errors = Column(Integer,default=0)
    ABSspeed = Column(Integer,default=1)
    speedx = Column(Integer,default=0)
    speedy = Column(Integer,default=0)
    def __init__(self, name, adres):
        self.name = name
        self.adres = adres
class LocalPlayer():
    def __init__(self,id,name,sock,adres):
        self.id = id
        self.name=name
        self.sock=sock
        self.adres=adres
        self.DB = s.get(Players,self.id)
        self.x=500
        self.y=500
        self.size=50
        self.errors=0
        self.ABSspeed=1
        self.speedx=0
        self.speedy=0
Base.metadata.create_all(engine)
Session = sessionmaker(engine)
s = Session()
main_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
main_socket.bind(('localhost',10000))
main_socket.setblocking(False)
main_socket.listen(5)
print ('socket создан')
plaers = { }
while True:
    try:
        new_socket, addr = main_socket.accept()
        print('Подключился', addr)
        new_socket.setblocking(False)
        plaers.append(new_socket)
    except BlockingIOError:
        pass
    for sock in plaers:
        try:
            data = sock.recv(1024).decode()
            print (data)
        except:
            pass   
    for sock in plaers:
        try:
            sock.send("1".encode())
        except:
            plaers.remove(sock)  
            sock.close()







