# tcp_client.py
import socket

HOST = "127.0.0.1"
PORT = 9000

def recv_line(sock: socket.socket) -> str:
    buf = b""
    while b"\n" not in buf:
        chunk = sock.recv(4096)
        if not chunk:
            raise ConnectionError("Server closed connection")
        buf += chunk
    line, _rest = buf.split(b"\n", 1)
    return line.decode("utf-8")

if __name__ == "__main__":
    with socket.create_connection((HOST, PORT), timeout=3) as s:
        s.sendall(b"hello from client\n")
        print("Server:", recv_line(s))
