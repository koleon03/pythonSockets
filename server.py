import socket
import selectors
import types

def accept_wrapper(socket):
    conn, addr = socket.accept()
    print("Accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print("Closing connection to", data.addr)
            sel.unregister(sock)


HOST = '127.0.0.1'
PORT = 456

sel = selectors.DefaultSelector()

print("Setting up server!")
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST,PORT))
lsock.listen()
print("Listening on", (HOST,PORT))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data = None)

while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:

