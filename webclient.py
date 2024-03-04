import socket
import argparse
import itertools

ENCODING='ISO-8859-1'
CRLF='\r\n'

# site port
parser = argparse.ArgumentParser(description="Web Client")
parser.add_argument('address', type=str, help="server host")
parser.add_argument('port', type=int, help="server port", default=443)

args = parser.parse_args()

request = (
    f'GET / HTTP/1.1\r\n'
    f'Host: {args.address}\r\n'
    f'Connection: close\r\n'
    f'\r\n'
).encode(ENCODING)

s = socket.socket()
s.connect((args.address, args.port))
s.sendall(request)

# can I with(socket...):
result = []
while True:
    data = s.recv(4096).decode(ENCODING)
    if len(data) == 0:
        break
    result += data
s.close()

print('RESULT')
print(''.join(result))

