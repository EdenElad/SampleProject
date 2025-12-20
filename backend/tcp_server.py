#tcp_server.py
import socket
import threading
from typing import Callable, Optional


Handler = Callable[[str], str]


class TcpLineServer:
    """
    TCP server שמדבר בפרוטוקול פשוט:
    כל הודעה היא שורה שמסתיימת ב-\n
    על כל שורה הוא מחזיר שורה (גם עם \n).
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 0,  # 0 = תן למערכת לבחור פורט פנוי (נוח לטסטים)
        handler: Optional[Handler] = None,
    ):
        self.host = host
        self.port = port
        self.handler = handler or (lambda s: s.upper())

        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._sock: Optional[socket.socket] = None

    def start(self) -> None:
        if self._thread is not None:
            raise RuntimeError("Server already started")

        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((self.host, self.port))
        srv.listen(128)
        srv.settimeout(0.2)  # כדי שנוכל לעצור בצורה נקייה

        self._sock = srv
        self.port = srv.getsockname()[1]  # הפורט האמיתי אם נתנו 0

        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None
        self._sock = None

    def _serve(self) -> None:
        assert self._sock is not None
        while not self._stop.is_set():
            try:
                conn, addr = self._sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break  # socket נסגר
            threading.Thread(
                target=self._handle_client, args=(conn, addr), daemon=True
            ).start()

    def _handle_client(self, conn: socket.socket, addr) -> None:
        buf = b""
        with conn:
            while not self._stop.is_set():
                try:
                    chunk = conn.recv(4096)
                except OSError:
                    break
                if not chunk:
                    break

                buf += chunk
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)

                    # מגבלת גודל לשורה (אופציונלי)
                    if len(line) > 10_000:
                        conn.sendall(b"ERR line too long\n")
                        continue

                    try:
                        msg = line.decode("utf-8")
                    except UnicodeDecodeError:
                        conn.sendall(b"ERR invalid utf-8\n")
                        continue

                    resp = self.handler(msg)
                    conn.sendall((resp + "\n").encode("utf-8"))


if __name__ == "__main__":
    server = TcpLineServer(host="127.0.0.1", port=9000)
    server.start()
    print(f"TCP server running on {server.host}:{server.port}")
    print("Press Ctrl+C to stop.")
    try:
        while True:
            threading.Event().wait(1.0)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        server.stop()
