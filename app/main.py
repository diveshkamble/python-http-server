# Uncomment this to pass the first stage
import socket


def main():
    """Main function"""
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client

    while True:
        client, _ = server_socket.accept()

        req = client.recv(1024).decode("utf-8")
        path = get_path(req)

        if path == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif "/echo" in path:
            resp_string = path.split("/", 2)[2]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(resp_string)}\r\n\r\n{resp_string}".encode()

        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        client.sendall(response)
        client.close()


def get_path(req: bytes) -> str:
    """Extracts path from request"""
    lines = req.split("\r\n")
    if lines:
        path = lines[0].split(" ")
        if len(path) > 1:
            return path[1]

    return "/"


if __name__ == "__main__":
    main()
