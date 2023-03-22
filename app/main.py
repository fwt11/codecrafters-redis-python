# Uncomment this to pass the first stage
import socket 


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    (conn, address) = server_socket.accept() # wait for client
    (buf, address) = conn.recvfrom(1024)
    buf = buf.split(b'\r\n')
    if buf[1] == b'$4' and buf[2] ==  b'ping':
        conn.sendall(b'+PONG\r\n')
    print(buf)


if __name__ == "__main__":
    main()
