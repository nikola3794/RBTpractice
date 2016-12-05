'''
z3-serial-port.py
'''

import struct

STX = 2

def process(byte, buffer):

    if buffer.__len__() == 0:

        if byte == STX:

            buffer.append(byte)

    else:

        if buffer.__len__() >=3 and buffer.__len__() == (buffer[2]+4):
            crc = buffer[0]

            for el in buffer[1:-1]:

                crc ^= el

            if crc == buffer[-1]:

                print(buffer)
                buffer.clear()
            else:

                print("Error")
                buffer.clear()

        else:
            buffer.append(byte)


def main():

    # Try's to read the message from the binary file
    try:
        fh = open('message.bin', 'rb')

    except IOError as e:
        print(e)

    else:
        buffer = bytearray()  # Buffer for the incoming bytes

        stx = False  # True - message currently in transmission ; False - no message currently in transmission

        while True:

            r = fh.read(1)

            if r != b'':

                byte = struct.unpack('B', r)[0]

                process(byte, buffer)

            else:
                print("EOF")
                break


        print(buffer)
        fh.close()









if __name__ == "__main__":
    main()