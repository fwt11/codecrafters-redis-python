# Uncomment this to pass the first stage
import socket 
import sys

storage = dict()


def reply_simple_string(conn, r):
    conn.sendall(b'+' + r + b'\r\n')


def reply_bulk_string(conn, r):
    conn.sendall(b"$" + str(len(r)).encode() + b'\r\n' + r + b'\r\n')


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
    global storage
    try:
        buff= conn.recv(4096)
        if not buff:
            return
        buff = buff.split(b"\r\n")

        command = buff[2].lower()
        print(command)

        if command == b'echo':
            conn.sendall(buff[3] + b"\r\n" + buff[4] + b"\r\n")
        elif command == b'set':
            if result := storage.get(buff[4]):
                storage[buff[4]] = buff[6]
                print(result)
                reply_bulk_string(conn, result)
            else:
                storage[buff[4]] = buff[6]
                conn.sendall(b'+OK\r\n')
        elif command == b'get':
            reply_bulk_string(conn, storage[buff[4]])
        elif command == b'ping':            
            reply_simple_string(conn, b'PONG')
    except BlockingIOError as e:
        return
    






if __name__ == "__main__":
    main()
