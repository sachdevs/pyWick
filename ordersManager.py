import socket
import sys
import time
    
def run(user, password, *commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            return rline.strip()
            rline = sfile.readline()
    finally:
        sock.close()

def subscribe(user, password):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\nSUBSCRIBE\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()

##################################################################
#        Scrapes historical data from Yahoo Finance API
##################################################################
def pullData(stock):
    try:
        fileLine = run("SpeedTraders", "speedtraders", "ORDERS "+stock)
        
        bidArr = []
        askArr = []

        datas = fileLine.split(" ")
        isBid = False
        i = 0
        for data in datas:
            if not(data == "SECURITY_ORDERS_OUT BID" or data == stock):
                if data == "BID":
                    isBid = True
                elif data == "ASK":
                    isBid = False
                elif isBid:
                    bidArr.append(data)
                elif not isBid:
                    askArr.append(data)
        askArr = askArr[1:]
        bidArr = bidArr[::2]
        askArr = askArr[::2]

        print bidArr
        print askArr
        print fileLine

        # Debugging statements
        print 'Pulled', stock
        print 'sleeping'
        # Time b/w each pull
        time.sleep(1)
        retAvg = (float(bidArr[0])+float(askArr[0]))/2
        return retAvg

    except Exception, e:
        print 'main loop', str(e)


##################################################################
#         range openp highp lowp volume closep Call
##################################################################
def ThirtySecondPrice(stock):
    priceList = []
    for i in range(0,30):
        x = pullData(stock)
        priceList.append(x)
    openp = priceList[0]
    highp = max(priceList)
    lowp = min(priceList)
    closep = priceList[len(priceList)-1]
    print openp, ' ', highp, ' ', lowp,  ' ', closep

ThirtySecondPrice('EA')