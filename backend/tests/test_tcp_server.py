import socket
import pytest
from backend.tcp_server import TcpLineServer


def recv_line(sock: socket.socket, timeout: float = 2.0) -> str:
    sock.settimeout(timeout)
    buf = b""
    while b"\n" not in buf:
        chunk = sock.recv(4096)
        if not chunk:
            raise ConnectionError("Server closed connection")
        buf += chunk
    line, _ = buf.split(b"\n", 1)
    return line.decode("utf-8")


@pytest.fixture()
def server():
    srv = TcpLineServer(host="127.0.0.1", port=0, handler=lambda s: s.upper())
    srv.start()
    yield srv
    srv.stop()


def test_echo_uppercase(server: TcpLineServer):
    with socket.create_connection((server.host, server.port), timeout=2) as s:
        s.sendall(b"hello\n")
        assert recv_line(s) == "HELLO"


def test_multiple_lines(server: TcpLineServer):
    with socket.create_connection((server.host, server.port), timeout=2) as s:
        s.sendall(b"a\nb\nc\n")
        assert recv_line(s) == "A"
        assert recv_line(s) == "B"
        assert recv_line(s) == "C"


def test_invalid_utf8(server: TcpLineServer):
    with socket.create_connection((server.host, server.port), timeout=2) as s:
        s.sendall(b"\xff\xfe\n")
        assert recv_line(s) == "ERR invalid utf-8"
