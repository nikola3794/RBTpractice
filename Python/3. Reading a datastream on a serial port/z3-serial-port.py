'''
fh=open('file.txt','wb')
s=bytearray()
s.append(2)
s.append(72)
s.append(10)
s.append(80)
s=s+b'lalala'
fh.write(s)

fh.close()

fh=open('file.txt','rb')
print(fh.read().decode())
'''
import time
import struct

def main():
    fh=open('file.txt','rb')

    while True:
        a=fh.read(1)

        if (a == b''):
            break

        print(a)
        num=struct.unpack('B', a)[0]
        print(num)
        time.sleep(1)





if __name__ == "__main__":
    main()
