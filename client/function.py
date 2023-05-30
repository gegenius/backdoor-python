#import
import os
import sys
import zlib
import socket
from cryptography.fernet import Fernet

#classe che gestisce il socket
class Connection:
    def __init__(self):
        self.sock = None
        self.conn = None
        self.ip = ""
        self.stat = False
        self.infoclient = None
        self.port = 10000
        self.criptokey = Fernet(b'PwgEU6_d09vEPRrFpLgtnUf_ixxUxThA94Ma31823iI=')

    # comandi della connessione

    def LISTEN(self):
        try:
            self.conn , self.infoclient = self.sock.accept()
            return True
        except:
            return False

    def INIT_CONN(self):
        #try:
            self.sock = socket.socket()
            self.sock.bind((self.ip, self.port))
            self.sock.listen(1)
            return True
        #except:
         #   return False

    def CLOSE_CONN(self):
        try:
            self.conn.close()
            return True
        except:
            return False



    def Ip_Targhet(self):
        try:
            return self.ip
        except:
            return False

    def Port(self):
        try:
            return self.port
        except:
            return False

    def Stat_Conn(self):
        try:
            return self.stat
        except:
            return False




    def SEND(self, data):
        try:
            data = data.encode()
        except:
            pass
        try:
            crc32 = zlib.crc32(data).to_bytes(6, 'big').replace(b'@', b'a')
            data = self.criptokey.encrypt(data)
            packet = data + b'@' + crc32 + b'@finish'
            self.conn.send(packet)
            return True
        except:
            return False

    def RECV(self):
        try:
            data = b''
            while True:
                try:
                    packet = self.conn.recv(4080)
                except:
                    sys.exit()

                data = data + packet

                if len(data.split(b'@')) >= 3:
                    if data.split(b'@')[-1] == b'finish':
                        break

            data = data.split(b'@')
            crc32 = data[-2]
            data.pop(-1)
            data.pop(-1)
            payload = b''
            for index in data:
                payload = payload + index + b'@'
            payload = payload.decode("ascii", "ignore")
            payload = list(payload)
            payload.pop(-1)
            payload = "".join(payload)
            payload = payload.encode()
            payload = self.criptokey.decrypt(payload)
            if zlib.crc32(payload).to_bytes(6, 'big').replace(b'@', b'a') != crc32:
                return False
            else:
                return payload
        except:
            return False