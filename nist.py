import socket
from datetime import datetime

# int.from_bytes([255], 'big')
# n = 0x0102
# n.to_bytes(2, 'big')

s = socket.socket()
s.connect(('time.nist.gov', 37))

result = b''
while True:
    # NIST should only send 4 bytes
    data = s.recv(4096)
    if len(data) == 0:
        s.close()
        break
    result += data

ts = int.from_bytes(result, "big")
now = datetime.utcnow()

# Nist does seconds since 1900-01-01
# Number of seconds between 1900-01-01 and 1970-01-01
nist_offset = 2208988800

print(f'TS: {ts}')
print(f'Nist time: {datetime.utcfromtimestamp(ts - nist_offset)}')
print(f'UTC time : {now}')

