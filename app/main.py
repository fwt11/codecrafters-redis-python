# Uncomment this to pass the first stage
import socket 
import sys
import time

storage = dict()


def reply_simple_string(conn, r):
    conn.sendall(b'+' + r + b'\r\n')


def reply_bulk_string(conn, r):
    conn.sendall(b"$" + str(len(r)).encode() + b'\r\n' + r + b'\r\n')


def reply_null_bulk_string(conn):
    conn.sendall(b"$-1\r\n")


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
        pass


    

def handle_client(conn):
    global storage
    try:
        buff = conn.recv(4096)
        if not buff:
            return
        buff = buff.split(b"\r\n")

        command = buff[2].lower()
        print(buff)
        print(command)

        if command == b'echo':
            conn.sendall(buff[3] + b"\r\n" + buff[4] + b"\r\n")
        elif command == b'set':
            value = buff[6]
            if len(buff) > 8 and buff[8].lower() == b"px":
                value  = (value, int(time.time()) + int(buff[10]))
                conn.sendall(b'+OK\r\n')
            elif result := storage.get(buff[4]):
                reply_bulk_string(conn, result)
            else:
                conn.sendall(b'+OK\r\n')
            storage[buff[4]] = value
        elif command == b'get':
            print(storage)
            value = storage.get(buff[4])
            print('value: ', value)
            if value:
                if isinstance(value, tuple):
                    if int(time.time()) > value[1]:
                        del storage[buff[4]]
                        reply_null_bulk_string(conn)
                        return
                    else:
                        value = value[0]
                reply_bulk_string(conn, value)
            else:
                reply_null_bulk_string(conn)     
        elif command == b'ping':            
            reply_simple_string(conn, b'PONG')
        else:
            reply_simple_string(conn, b'PONG')
    except BlockingIOError as e:
        return
    






if __name__ == "__main__":
    main()
