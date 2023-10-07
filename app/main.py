# Uncomment this to pass the first stage
import os
import socket
import sys
import threading
from typing import Any


def get_path(req: bytes) -> str:
    """Extracts path from request"""
    lines = req.split("\r\n")
    if lines:
        path = lines[0].split(" ")
        if len(path) > 1:
            return path[1]

    return "/"


def get_user_agent(req: bytes) -> str:
    """Extracts user-agent from request"""
    for line in req.split("\r\n"):
        if line.startswith("User-Agent:"):
            user_agent = line.split(" ", 2)[1]
            return user_agent
    return ""


def handle_connections(client: socket, addr: Any):
    "Takes in connection"
    req = client.recv(1024).decode("utf-8")
    path = get_path(req)
    if path == "/":
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    elif "/echo" in path:
        resp_string = path.split("/", 2)[2]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(resp_string)}\r\n\r\n{resp_string}".encode(
            "utf-8"
        )
    elif "/user-agent" in path:
        user_agent = get_user_agent(req)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode(
            "utf-8"
        )
    elif "/files" in path:
        filename = path.split["/"][-1]
        directory = sys.argv[-1]
        if os.path.exists(directory + filename):
            with open(directory + filename, "rb") as file:
                body = file.read()
        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {os.path.getsize(directory+filename)}\r\n\r\n{body}".encode(
            "utf-8"
        )
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    client.sendall(response)
    client.close()


def main():
    """Main function"""
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #

    # server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client

    while True:
        client, addr = server_socket.accept()
        threading.Thread(target=handle_connections, args=(client, addr)).start()


if __name__ == "__main__":
    main()
