import socket
from console import Console, to_thread
import logging
import utils



_log = logging.getLogger(__name__)
_log.addHandler(utils.HANDLER)
_log.setLevel(logging.INFO)


class Server:
    def __init__(self, hostname, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Allow reused afterwards
        self.server_socket.bind((hostname, port))
        self.server_socket.listen(1)
        self.client_socket, self.address = None,None
        self.buffer = []

    class ConnectionBrokenException(Exception):
        pass

    @to_thread
    def connect(self):
        (self.client_socket, self.address) = self.server_socket.accept()


    def disconnect(self):
        self.server_socket.shutdown(socket.SHUT_RDWR)
        self.server_socket.close()

    def receive_line(self):
        chunks = []

        while len(self.buffer) > 0:
            buffered = self.buffer.pop()
            if b'\n' in buffered:
                i = buffered.index(b'\n')
                chunks.append(buffered[:i])
                self.buffer.append(buffered[i + 1:])
                return b''.join(chunks)
            else:
                chunks.append(buffered)

        while True:
            chunk = self.client_socket.recv(1024)
            if not chunk:
                raise Server.ConnectionBrokenException()

            if b'\n' in chunk:
                i = chunk.index(b'\n')
                chunks.append(chunk[:i])
                self.buffer.append(chunk[i + 1:])
                return b''.join(chunks)
            else:
                chunks.append(chunk)

    def send_line(self, msg):
        if not msg.endswith("\n"):
            msg = msg + "\n"
        msg = msg.encode()

        total_sent = 0
        while total_sent < len(msg):
            sent = self.client_socket.send(msg[total_sent:])
            if sent == 0:
                raise Server.ConnectionBrokenException()
            total_sent = total_sent + sent
            
            
class WebSocketConsole:
    
    def __init__(self, console: Console, hostname, port) -> None:
        self.SERVER = Server(hostname,port)
        self.CONSOLE = console

    async def start(self):
        while self.CONSOLE.online:
            _log.debug("WebSocket Open...")
            try:
                await self.SERVER.connect()
                _log.info("WebSocket Connected!")
                try:
                    await self.CONSOLE.start(self.get_socket_input)
                except Server.ConnectionBrokenException:
                    _log.info("WebSocket Disconnected!")
            except OSError:
                _log.debug("Socket waiting for connection was interupted.")

    
    def stop(self):
        self.SERVER.disconnect()

    def get_socket_input(self) -> list[str]:
        """ Receives input via the client socket connected to the server_socket of the main program.
        @returns a list containing a command and its arguments.
        @raises Server.ConnectionBrokenException when the socket disconnects.
        """
        instruction = self.SERVER.receive_line().decode()
        self.SERVER.send_line("200/OK")
        return instruction.split(" ")