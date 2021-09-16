#!/usr/bin/env python3
import socket
import socket, sys

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip
    
    
def main():
    #define address info, payload, and buffer size
    external_host = 'www.google.com'
    port = 80
        
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Start proxy server")
        
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(2)
        
        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("connecting to Google")
                remote_ip = get_remote_ip(external_host)
            	
                proxy_end.connect((remote_ip, port))
                # send data
                send_full_data = conn.recv(BUFFER_SIZE)
                print(f"sending recieved data {send_full_data} to Google")
                proxy_end.sendall(send_full_data)

                proxy_end.shutdown(socket.SHUT_WR)
                data = proxy_end.recv(BUFFER_SIZE)
                print(f"sending recieved data {data} to client")
                # send data back to client 
                conn.send(data)

            conn.close()

if __name__ == "__main__":
    main()

             	
        	
        
