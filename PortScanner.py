#!/usr/bin/python

# Author Mahdi Robatipoor
# mahdi.robatipoor@gmail.com

import argparse,sys,socket,threading

timeOut = 5
screenLock = threading.Semaphore(1)
red = '\033[31m'
green = '\033[32m'

def checkOpenPort(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeOut)
    try:
        sock.connect((ip, port))
        screenLock.acquire()
        print('%s [+] %s : Port %d Open ' % (green,ip,port))
    except Exception as ex:
        screenLock.acquire()
        print('%s [-] %s : Port %d Close ' % (red,ip, port))
        print(ex)
    finally:
        screenLock.release()
        sock.close()

def scanPort(hostname,ports):
    try:
        ip = socket.gethostbyname(hostname)  # get IP address target
    except Exception as ex:
        print(ex)
        sys.exit(1)
    if len(ports) == 2:
        if ports[0] < ports[1]:
            max_range = ports[1]
            max_range += 1
            range_port = range(ports[0],max_range)
        else:
            max_range = ports[0]
            max_range += 1
            range_port = range(ports[1], max_range)
    elif len(ports) == 1:
        range_port = ports
    else:
        print('%sPlease Enter Correct Option'%(red))
        sys.exit(1)

    for p in range_port:
        thread = threading.Thread(target=checkOpenPort,args=(ip,p))
        thread.start()

def main():
    global timeOut
    mnp = 65535  # maximum number port
    example = 'to example scan range ports 20 util 100 google => python %(prog)s -H google.com -p 20 100'
    parser = argparse.ArgumentParser(description=example)
    parser.add_argument('-H','--host',dest='host',type=str)
    parser.add_argument('-p','--port',dest='port',type=int,nargs='+')
    parser.add_argument('-t', '--timeout', dest='timeOut', type=int,default=5,required=False)
    parser.add_argument('-v','--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    if args.host != None and args.port != None: # check not null option
        if max(args.port) <= mnp and min(args.port) >= 1: # check exist in range port number
            timeOut = args.timeOut
            scanPort(args.host, args.port)
    else:
        print('%s Error !!!'%(red))
        parser.print_help()
        sys.exit(1)
if __name__ == '__main__':
    main()

