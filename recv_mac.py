import socket, struct

def get_my_add():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	my_ip=s.getsockname()[0]
	s.close()

	from uuid import getnode as get_mac
	mac = get_mac()
	my_mac=[]
	for i in range(1,7): my_mac.append(mac>>8*(6-i)&0xff)
	return [my_ip, my_mac]

def send_arp(src_mac, src_ip, dst_mac, dst_ip, opcode, n):
	sock=socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
	sock.bind(("eth0", 0))

	packet=""
	ETHERNET_FRAME=[	
     		struct.pack('!6B',dst_mac[0],dst_mac[1],dst_mac[2],dst_mac[3],dst_mac[4],dst_mac[5]), 
        	struct.pack('!6B',src_mac[0],src_mac[1],src_mac[2],src_mac[3],src_mac[4],src_mac[5]),	
       	struct.pack('!H',0x0806)
	]
	ARP_FRAME=[
		struct.pack('!H', 0x0001),
		struct.pack('!H', 0x0800),
		struct.pack('!B', 0x06),
		struct.pack('!B', 0x04),
		struct.pack('!H', opcode),
		struct.pack('!6B',src_mac[0],src_mac[1],src_mac[2],src_mac[3],src_mac[4],src_mac[5]),	
		struct.pack('!4B',src_ip[0],src_ip[1],src_ip[2],src_ip[3]),					
		struct.pack('!6B',dst_mac[0],dst_mac[1],dst_mac[2],dst_mac[3],dst_mac[4],dst_mac[5]),	
		struct.pack('!4B',dst_ip[0],dst_ip[1],dst_ip[2],dst_ip[3])					
	]
	for i in range(0,3): packet+=ETHERNET_FRAME[i]
	for i in range(0,9): packet+=ARP_FRAME[i]
	for i in range(0,n): sock.send(packet)
	sock.close()

src_mac=[]
dst_mac=[]
src_ip=[]
dst_ip=[]
for i in range(6): src_mac.append(0xaa)
for i in range(6): dst_mac.append(0xbb)
for i in range(4): src_ip.append(127)
for i in range(4): dst_ip.append(8)
send_arp(src_mac, src_ip, dst_mac, dst_ip, 3, 10)
