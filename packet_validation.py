
root = './tcp_data'
def route_info(i: int):
    filepath = f'{root}/tcp_addrs_{i}.txt'
    with open(filepath, 'r') as f:
        (src, dest) = f.readline().split(' ')
        src = b''.join([int(n).to_bytes(1, 'big') for n in src.split('.')])
        dest = b''.join([int(n).to_bytes(1, 'big') for n in dest.split('.')])

    return (src, dest)


def open_packet(i: int):
    filepath = f'{root}/tcp_data_{i}.dat'
    with open(filepath, 'rb') as f:
        data = f.read()
    return data

def make_header(src: bytes, dest: bytes, tcp_length: int) -> bytes:
# IP Pseudo Header... 12 bytes
# +--------+--------+--------+--------+
# |           Source Address          |
# +--------+--------+--------+--------+
# |         Destination Address       |
# +--------+--------+--------+--------+
# |  Zero  |  PTCL  |    TCP Length   |
# +--------+--------+--------+--------+
    ZERO = 0x00.to_bytes(1, 'big')
    PTCL = 0x06.to_bytes(1, 'big') # 6 = TCP
    return src + dest + ZERO + PTCL + tcp_length.to_bytes(2, 'big')


def compare():
    # 0-4 should pass, 5-9 should fail
    for i in range(10):
        (src, dest) = route_info(i)
        packet = open_packet(i)
        header = make_header(src, dest, len(packet))
        checksum_bytes = int.from_bytes([packet[16], packet[17]], 'big')
        zero_checksum = packet[:16] + b'\x00\x00' + packet[18:]
        # Must be even length 
        if len(zero_checksum) % 2 != 0:
            zero_checksum += b'\x00'

        payload = header + zero_checksum

        total = 0
        offset = 0
        while offset < len(payload):
            word = int.from_bytes(payload[offset:offset + 2], 'big')
            total += word
            # one's complement sum
            total = (total & 0xFFFF) + (total >> 16)
            offset += 2
        # 1's complement of the sum
        total = (~total) & 0xFFFF # binary NOT and 16bit mask

        print(checksum_bytes == total)

if __name__ == '__main__':
    compare()

