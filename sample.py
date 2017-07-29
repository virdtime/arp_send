import socket, struct, binascii

sc=socket.socket(socket.AF_PACKET,socket.SOCK_RAW, socket.htons(0x0003))
i=0
ip_l=[]
arp_t={}

while True:
    
    packet=sc.recvfrom(42)
    ethr=packet[0][0:14]
    eth=struct.unpack("!6s6s2s",ethr)

    ethertype=eth[2]
    arpr=packet[0][14:42]
    arp=struct.unpack("!2s2sss2s6s4s6s4s",arpr)
    if ethertype != '\x08\x06':
        continue
    if arp[4]!='\x00\x02':
	  continue
    i+=1

    if ~(ip_l.count(socket.inet_ntoa(arp[6])[-3:])):
	ip_l.append(socket.inet_ntoa(arp[6])[-3:])
	arp_t[socket.inet_ntoa(arp[6])[-3:]]=binascii.hexlify(arp[5])
   
    if arp_t[socket.inet_ntoa(arp[6])[-3:]]!=binascii.hexlify(arp[5]):
	print 'arp detected!!'
	break

    if i==10:
	arp_t={}
	ip_l=[]
	i=0
