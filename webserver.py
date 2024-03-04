import socket
import argparse
import os
from typing import Union

ENCODING='ISO-8859-1'
CRLF='\r\n'

parser = argparse.ArgumentParser(description="Web Client")
parser.add_argument('port', type=int, help="server port", default=28333)

args = parser.parse_args()
server_root = os.path.abspath('.')
# Learning, can't use: 
#   socket.create_connection()
#   socket.create_server()
#   urllib


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', args.port)) # '' = localhost
s.listen()

# TODO: how to know when to split on text/application/etc for files?
mime_types = {
    'txt': 'text/plain',
    'html': 'text/html',
    'css': 'text/css',
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
}
status_codes = {
    200: 'OK',
    404: 'NOT FOUND',
}

# TODO: make either type (I miss Scala sometimes...)
def get_file_contents(path: str) -> Union[None, tuple[str, bytes]]:
    full_path = os.path.sep.join([server_root, path])
    full_path = os.path.abspath(full_path)
    if not full_path.startswith(server_root):
        return None
    (file_path, file_name) = os.path.split(full_path)
    (name, file_ext) = os.path.splitext(file_name)
    file_ext = file_ext[1::]
    try:
        # TODO: make generator?
        with open(full_path, 'rb') as f:
            mime_type = mime_types.get(file_ext, 'text/plain')
            return (mime_type, f.read())
    except:
        return None

def make_response(code: int, content_type: str, content: bytes):
    code_text = status_codes.get(code, 'UNKNOWN STATUS')
    # TODO: Handle errors and responses better
    #if 200 <= code < 300:
    return (
        f'HTTP/1.1 {code} {code_text}{CRLF}'
        f'Content-Type: {content_type}{CRLF}'
        f'Content-Length: {len(content)}{CRLF}'
        f'Connection: close{CRLF}'
        f'{CRLF}'
        #f'{content}'
    ).encode(ENCODING) + content


def process_headers(headers: str):
    pass

# TODO: Sep headers from body
# TODO: Extract into functions
# TODO: Split Verbs into functions
# TODO: All the error checking, Try/Excepts
# TODO: Can I use socket as a resource?
while True:
    (soc, return_adddress) = s.accept()
    headers = ''
    body = []
    print(f'Connection Recieved From: {return_adddress}')
    while True:
        data = soc.recv(4096).decode(ENCODING)
        headers += data
        # Reached End of Header
        if ''.join(headers[-4::]) == '\r\n\r\n':
            header_lines = headers.split(CRLF)
            (method, path, protocol) = header_lines[0].split(' ')
            content = get_file_contents(path)
            if content is None:
                response = make_response(404, 'text/plain', b'404 not found')
            else:
                (mime, body) = content
                response = make_response(200, mime, body)
    
            soc.sendall(response)
            soc.close()
            headers = ''
            break

s.close()


