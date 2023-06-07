#import
import os
import sys
import zlib
import socket
from cryptography.fernet import Fernet

#classe che gestisce il socket
class Connection:

    #variabili comuni della classe
    def __init__(self):
        self.sock = None
        self.conn = None
        self.ip = ""
        self.stat = False
        self.infoclient = None
        self.port = 10000
        self.criptokey = Fernet(b'PwgEU6_d09vEPRrFpLgtnUf_ixxUxThA94Ma31823iI=')

    #in ascolto sulla porta 10000
    def LISTEN(self):
        try:
            self.conn , self.infoclient = self.sock.accept()
            return True
        except:
            return False

    #inizializzazione socket
    def INIT_CONN(self):
        try:
            self.sock = socket.socket()
            #self.sock.settimeout()
            self.sock.bind((self.ip, self.port))
            self.sock.listen(1)
            return True
        except:
            return False

    #chiusura connessione
    def CLOSE_CONN(self):
        try:
            self.conn.close()
            return True
        except:
            return False

    #return ip targhet
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

    #return stato connessione (True False)
    def Stat_Conn(self):
        try:
            return self.stat
        except:
            return False


    #invio di pacchetti
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
            self.conn.send(packet)
            return True
        except:
            return False

    #recezione dati
    def RECV(self):
        try:
            data = b''
            c = 0
            #recezione pacchetti in loop
            while True:
                c = c + 1
                try:
                    packet = self.conn.recv(4080)
                except:
                    return "recv err"
                    sys.exit()

                if packet == b'':
                    return "recv err"
                    sys.exit()

                #sommario pacchetti
                data = data + packet

                if c % 100 == 0:
                    print("[*] dimensione pacchetti ricevuti del frame " + str(sys.getsizeof(data) / 1000000) + " MB")

                #controllo integrità pacchetto
                if len(data.split(b'@')) >= 3:
                    if data.split(b'@')[-1] == b'finish':
                        break

            #separazione di crc32 e payload (decriptato)
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
            #verifica dell pacchetto
            if zlib.crc32(payload).to_bytes(6, 'big').replace(b'@', b'a') != crc32:
                return False
            else:
                return payload
        except:
            return False



#struttura pacchetto
#b'[ payload criptato ]@[ crc32 ]@finish'