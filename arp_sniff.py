import socket, struct, binascii

class ethernet_h:
    def set_header(self, packet):
        ethr=packet[0][0:14]
        eth=struct.unpack("!6s6s2s",ethr)
        self.dest_mac=eth[0]
        self.srce_mac=eth[1]
        self.ether_type=eth[2]

class arp_h:
    def set_header(self, packet):
        arpr=packet[0][14:42]
        arp=struct.unpack("!2s2sss2s6s4s6s4s",arpr)
        self.h_type=arp[0]
        self.p_type=arp[1]
        self.h_len=arp[2]
        self.p_len=arp[3]
        self.opcode=arp[4]
        self.src_mac=arp[5]
        self.src_ip=arp[6]
        self.dst_mac=arp[7]
        self.dst_ip=arp[8]

raw=socket.socket(socket.AF_PACKET,socket.SOCK_RAW, socket.htons(3))
while True:
    pac=raw.recvfrom(42)
    ethn=ethernet_h()
    ethn.set_header(pac)

    if ethn.ether_type != '\x08\x06':
        continue
    arp=arp_h()
    arp.set_header(pac)
    print binascii.hexlify(arp.opcode)
