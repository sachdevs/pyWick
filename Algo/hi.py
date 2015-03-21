import socket
import sys
import time
import pdb

HOST, PORT = "codebb.cloudapp.net", 17429
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

data = "SpeedTraders"+ " " + "speedtraders" +"\n"

sock.connect((HOST, PORT))
print'connected'
sock.sendall(data)

def run(*commands):
    data =  "\n".join(commands) + "\n"
    sock.sendall(data)
    sfile = sock.makefile()
    rline = sfile.readline()
    return rline.strip()

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


def parse():
    string = run("SECURITIES")
    data = string.split(" ")
    data = data[1:]
    struct = []
    lst = []
    i=0
    while i < len(data):
        n = i
        while n < 4+i:
            lst.append(data[n])
            n+=1
        struct.append(lst)
        lst = []
        i+=4
    return struct

def spread(stock):
    fileLine = run("ORDERS " + str(stock))
        
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
    #print ((float(askArr[0]) - float(bidArr[0]))/((float(askArr[0]) + float(bidArr[0]))/2))
    #return (float(askArr[0]) - float(bidArr[0]))/((float(askArr[0]) + float(bidArr[0]))/2)
    return 3.0

def ratio(struct):
    lst = []
    for i in range(0,9):
        if float(spread(struct[i][0])) == 0.0:
            lst.append((10000000, struct[i][0]))
        else:
            lst.append((float(struct[i][2])/float(spread(struct[i][0])), struct[i][0]))
    return lst

def budget():
    a = run("MY_CASH")
    print a
    return a

def buy(stock):
    priceToBuy = ""
    shareNum = ""
    lol = run("ORDERS " +str(stock))
    curr = lol.split(" ")
    for i in range(len(curr)):
        if curr[i] is "ASK":
            priceToBuy = curr[i+2]
            shareNum = curr[i+3]
            break
    run("BID "+ stock + " " + str(int(priceToBuy)+0.02) + " "+ shareNum)
    portfolio.append(stock)
    print 'buying '+ stock

portfolio = []

while True:
    bud = budget()
    struct = parse()
    lst = ratio(struct)
    lst = sorted(lst,key=lambda x: x[0])
    print lst
    if spread(lst[len(lst)-1]) <  float(lst[-1][4]):
        run("BID "+ lst[-1][1] + " " + (float(lst[len(lst)-1][0])+0.02) + " 10")


    print lst
    time.sleep(1)