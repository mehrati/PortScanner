#!/usr/bin/python

# Author Mahdi Robatipoor 
# mahdi.robatipoor@gmail.com

import argparse,sys,socket,threading

timeOut = 0
screenLock = threading.Semaphore(1)

def checkOpenPort(ip,port):
    global timeOut
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeOut)
    print(timeOut)
    try:
        sock.connect((ip, port))
        screenLock.acquire()
        print('[+] %s : Port %d Open ' % (ip,port))
    except Exception as ex:
        screenLock.acquire()
        print('[-] %s : Port %d Close ' % (ip, port))
        print(ex)
    finally:
        screenLock.release()
        sock.close()

def scanPort(hostname,ports):
    try:
        ip = socket.gethostbyname(hostname)
    except Exception as ex:
        print(ex)
        sys.exit(1)
    if len(ports) > 1:
        if ports[0] < ports[1]:
            max_range = ports[1]
            max_range += 1
            range_port = range(ports[0],max_range)
        else:
            max_range = ports[0]
            max_range += 1
            range_port = range(ports[1], max_range)
    else:
        range_port = ports

    for p in range_port:
        thread = threading.Thread(target=checkOpenPort,args=(ip,p))
        thread.start()

def main():
    global timeOut
    example = 'to example scan range ports 20 util 100 google => python %(prog)s -H google.com -p 20 100'
    parser = argparse.ArgumentParser(description=example)
    parser.add_argument('-H','--host',dest='host',type=str)
    parser.add_argument('-p','--port',dest='port',type=int,nargs='+',choices=range(1, 6550))
    parser.add_argument('-t', '--timeout', dest='timeOut', type=int,default=5,required=False)
    parser.add_argument('-v','--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    if args.host != None and args.port != None:
        scanPort(args.host, args.port)
        timeOut = args.timeOut
        print(timeOut)
    else:
        print('Error !!!')
        parser.print_help()
        sys.exit(1)
if __name__ == '__main__':
    main()

