import random

'''
Generates a message and stores it in a binary file.
'''
def generateMessage():
    x = bytearray()
    x = x + b'2578eguovu034hbh8w4vu1cj923'

    # 4 Correct messages
    for j in range(4):

        #Adds a command to the message
        x.append(2)  # STX byte
        x.append(random.randint(0,127))  # CMD
        len = 2 ** j
        x.append(len)  # DataLen
        for el in range(len):
            x.append(random.randint(0,255))  # D[i]

        # CRC byte is computed as a XOR of all the bytes in the message
        crc = 2
        for i in x[-(len + 2):]:
            crc ^= i
        x.append(crc)

        x = x + b'asdsfu69byhjv5ynvjtv4ny04h3nveh9v3huu395379tyvhb9jas'

    # 3 Incorrect messages
    for j in range(3):

        #Adds a command to the message
        x.append(2)  # STX byte
        x.append(random.randint(0,127))  # CMD
        len = 2 ** (j + 1)
        x.append(len)  # DataLen
        for el in range(len-1):
            x.append(random.randint(0,255))  # D[i]

        x = x + b'6789654345678987654rfgbnjhgfdfghjkkjgfd'

    # 1 Correct messages
    for j in range(1):

        # Adds a command to the message
        x.append(2)  # STX byte
        x.append(random.randint(0, 127))  # CMD
        len = 2 ** (j+2) #Len = 2
        x.append(len)  # DataLen
        for el in range(len):
            x.append(random.randint(0, 255))  # D[i]

        # CRC byte is computed as a XOR of all the bytes in the message
        crc = 2
        for i in x[-(len + 2):]:
            crc ^= i
        x.append(crc)

        x = x + b'lkjhgtr65789okljhgt678ijhgt678ijnbvgftr56789'

    # One half complete message
    x.append(2)  # STX byte
    x.append(random.randint(0, 127))  # CMD
    len = 2 ** (j + 2)
    x.append(len) # DataLen
    x.append(80)


    return x


def main():
    x=generateMessage()
    fileName='message.bin'

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