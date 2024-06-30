import socket
import selectors
import sys
import jinja2
import logging
import os

selector = selectors.DefaultSelector()
env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
logging.basicConfig(level=logging.DEBUG, datefmt='%d.%m.%Y %H:%M:%S',
                    format='[%(asctime)s] #%(levelname)- 5s - %(name)s - %(message)s'
                    )
logger = logging.getLogger(__name__)
HOST = '0.0.0.0'
PORT = 8080


def create_server(host: str, port: int):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        logger.info(f'server socket start , listen HOST: {host}, PORT: {port}')
        selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=(accept_connections, b''))
        logger.debug('selector register server socket')
    except Exception as e:
        logger.critical(f'Server not started, Errors: {e}')
        sys.exit(1)


def accept_connections(selector_key: selectors.SelectorKey):
    client_socket, addr = selector_key.fileobj.accept()
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=(read_request, b''))
    logger.debug(f'Client connect, address: {addr}')
    logger.debug(f'selector register client: {client_socket}')


def read_request(selector_key: selectors.SelectorKey):
    request = selector_key.fileobj.recv(1024)
    logger.debug(f'read request, chunk: {request.decode()}')
    selector.modify(fileobj=selector_key.fileobj, events=selectors.EVENT_READ,
                    data=(read_request, selector_key.data[1]+request))


def send_message(selector_key: selectors.SelectorKey):
    request = selector_key.data[1].decode()
    logger.debug(f'send message, request: {request}')
    lines = request.split('\n')[0].split()
    if lines and lines[0] == "GET" and (lines[1] == '/healthz' or lines[1] == '/healthz/'):
        response = env.get_template('index.html')
        response = response.render(msg='OK')
        response = (f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n"
                    f"Content-Length: {len(response)}\r\n\r\n{response}")
        selector_key.fileobj.send(response.encode())
    else:
        selector_key.fileobj.send(b'HTTP/1.1 404 Not Found\r\nConnection: close'
                                  b'\r\nContent-Type: text/plain\r\n\r\nNot Found')


def event_loop(host: str, port: int):
    create_server(host, port)
    while True:
        try:
            events = selector.select(timeout=0)
            for sock, _ in events:
                callback = sock.data[0]
                callback(sock)
            delete_socks = []
            for file_number in selector.get_map():
                socks = [key[0].fileobj for key in events]
                selector_key = selector.get_key(file_number)
                if not (selector_key.fileobj in socks) and selector_key.data[1]:
                    delete_socks.append(selector_key.fileobj)
                    send_message(selector_key)
            for sock in delete_socks:
                logger.debug(f'delete sockets: {delete_socks}')
                selector.unregister(sock)
                sock.close()
        except KeyboardInterrupt:
            break
    logger.info('Server Stop')


if __name__ == '__main__':
    event_loop(HOST, PORT)
