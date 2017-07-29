import struct,math

def inode(inode,iper,g,size,f):
    block_pointer=[]
    gdt=math.ceil(inode/iper)-1
    bunZ=inode%iper
    i=struct.unpack_from("<I",g,0x8+gdt*32)[0]*size
    f.seek(i+(bunZ-1)*0x100)
    da=f.read(0x100)
    file_mode=ord(struct.unpack_from("<c",da,0x1)[0])>>4
    file_size=struct.unpack_from("<I",da,0x4)[0]
    for i in range(15): block_pointer.append(struct.unpack_from("<I",da,0x28+i*0x4)[0]*0x1000)
    return {"file_mode":file_mode, "file_size":file_size, "block_pointer":block_pointer}

def analy(data,f_size):
    r=[]
    s=0
    while(s!=f_size):
        name=""
        inode=struct.unpack_from("<I",data,s)[0]
        size=struct.unpack_from("<H",data,4+s)[0]
        name_len=data[s+6]
        for i in range(name_len): name+= chr(data[i+s+8])
        r.append({"inode":inode,"name":name})
        s+=size
    return r

def direct(f,offset,f_size):
    f.seek(offset)
    data=f.read(f_size)
    return analy(data,f_size)
    

f=open('ext3.dd','rb')
f.seek(1024)
sp=f.read(1024)

block_size=struct.unpack_from("<l",sp,0x18)[0]
gdb_n=math.ceil(struct.unpack_from("<I",sp,0x4)[0]/struct.unpack_from("<I",sp,0x20)[0])
iper=struct.unpack_from("<l",sp,0x28)[0]

if block_size==0:
    size=1024
    gdb=2048
elif block_size==1:
    size=2048
    gdb=2048
elif block_size==2:
    size=4096
    gdb=4096

f.seek(gdb)
g=f.read(32*gdb_n)
R_inode=struct.unpack_from("<I",g,0x8)[0]*size

f.seek(R_inode+0x100)
sp=f.read(0x100)
d=struct.unpack_from("<I",sp,0x28)[0]*size

for i in range(7):
    print(direct(f,d,0x1000)[i].get("name"),inode(direct(f,d,0x1000)[i].get("inode"),iper,g,size,f))
    print()

