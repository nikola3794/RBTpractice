import random

'''
Generates a message and stores it in a binary file.
'''
def generateMessage():
    x = bytearray() # Create an empty message
    x = x + b'2578eguovu034hbh8w4vu1cj923' # Add random bytes to the message

    # Add 4 valid commands surrounded with random bytes to the message
    for j in range(4):

        # Start of a command
        x.append(2)  # STX byte
        x.append(random.randint(0,127))  # CMD
        len = 2 ** j
        x.append(len)  # DataLen

        for el in range(len):
            x.append(random.randint(0,255))  # D[i]

        # CRC byte is computed as a XOR of all the bytes in the command
        crc = 2
        for i in x[-(len + 2):]:
            crc ^= i
        x.append(crc)
        # End of a command

        x = x + b'asdsfu69byhjv5ynvjtv4ny04h3nveh9v3huu395379tyvhb9jas' # Add random bytes to the message

    # Add 3 invalid commands surrounded with random bytes to the message
    for j in range(3):

        # Start of a command
        x.append(2)  # STX byte
        x.append(random.randint(0,127))  # CMD
        len = 2 ** (j + 1)
        x.append(len)  # DataLen

        for el in range(len-1):
            x.append(random.randint(0,255))  # D[i]

        # The command lacks 1 additional data byte and 1 crc byte

        x = x + b'6789654345678987654rfgbnjhgfdfghjkkjgfd' # Add random bytes to the message

    # Add 1 valid command surrounded with random bytes to the message
    for j in range(1):

        # Start of a command
        x.append(2)  # STX byte
        x.append(random.randint(0, 127))  # CMD
        len = 5
        x.append(len)  # DataLen

        for el in range(len):
            x.append(random.randint(0, 255))  # D[i]

        # CRC byte is computed as a XOR of all the bytes in the message
        crc = 2
        for i in x[-(len + 2):]:
            crc ^= i
        x.append(crc)
        # End of a command

        x = x + b'lkjhgtr65789okljhgt678ijhgt678ijnbvgftr56789' # Add random bytes to the message

    # Add 1 half-complete command surrounded with random bytes to the message
    # Start of a command
    x.append(2)  # STX byte
    x.append(random.randint(0, 127))  # CMD
    len = 4
    x.append(len) # DataLen
    x.append(80) # D[1]

    # The command lacks 3 additional data byte and 1 crc byte

    return x


def main():
    fileName='message.bin' # File path of the binary file, where the message will be stored

    x = generateMessage()  # Generate the message to be stored

    #Trys to write the message to the binary file
    try:
        fh = open(fileName, 'wb')
    except IOError:
        print("Couldn't open ", fileName, " in wb mode.")
    else:
        fh.write(x)
        fh.close()

if __name__ == "__main__":
    main()