# Uncomment this to pass the first stage
import socket 
import sys


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    server_socket.setblocking(False)
    
    clients = []

    while True:
        try:
            conn, addr = server_socket.accept() # wait for client
            conn.setblocking(False)
            clients.append(conn)
        except BlockingIOError as e:
            pass

        for client in clients:
            handle_client(client)
    

def handle_client(conn):
    try:
        buff= conn.recv(4096)
        if not buff:
            return
        buff = buff.split(b"\r\n")
        if buff[2] == b'ECHO' or buff[2] == b'echo':
            conn.sendall(buff[3] + b"\r\n" + buff[4] + b"\r\n")

        conn.sendall(b'+PONG\r\n')
    except BlockingIOError as e:
        return



if __name__ == "__main__":
    main()
