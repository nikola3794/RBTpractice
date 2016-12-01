'''
Generates a message which is to be stored in a binary file and later processed.
'''
def generateMessage():
    x = bytearray()

    for j in range(3):

        x = x + b'ajsdfhjkdaskafjsk'

        #Adds a command to the message
        x.append(2)  # STX byte
        x.append(12)  # CMD = 12
        len = 3
        x.append(len)  # DataLen = 3
        x.append(80)  # D[0]
        x.append(79)  # D[1]
        x.append(80)  # D[2]

        # CRC byte is computed as a XOR of all the bytes in the message
        crc = 2
        for i in x[-(len + 2):]:
            crc = crc ^ i
        x.append(crc)

        x = x + b'ashjdfkjkadsfjas'

    return x


def main():
    x=generateMessage()
    fileName='message.txt'

    #Trys to write the message to a binary file
    try:
        fh = open(fileName, 'wb')
    except IOError:
        print("Couldn't open ", fileName, " in wb mode.")
    else:
        fh.write(x)
        fh.close()

if __name__ == "__main__":
    main()