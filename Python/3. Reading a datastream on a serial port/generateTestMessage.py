'''
generate-test-message.py
'''

import random

STX = 2

'''
Function: generateMessage
Inputs:
Outputs: msg

Generates a message - msg and outputs it.
'''
def generateMessage():

    msg = bytearray()  # Create an empty message

    # Add 4 valid commands surrounded with random bytes to the message
    for j in range(4):

        # Start of a command
        msg.append(STX)  # STX byte
        msg.append(random.randint(0, 127))  # CMD
        l = 2 ** j
        msg.append(l)  # DataLen

        for el in range(l):
            msg.append(random.randint(0, 255))  # D[i]

        # CRC byte is computed as a XOR of all the bytes in the command
        crc = STX
        for i in msg[-(l + 2):]:
            crc ^= i
        msg.append(crc)
        # End of a command

        msg += b'9js'  # Add random bytes to the message

    # Add 3 invalid commands surrounded with random bytes to the message
    for j in range(3):

        # Start of a command
        msg.append(STX)  # STX byte
        msg.append(random.randint(0, 127))  # CMD
        l = 2 ** (j + 1)
        msg.append(l)  # DataLen

        for el in range(l-1):
            msg.append(random.randint(0, 255))  # D[i]
        # The command lacks 1 additional data byte and 1 crc byte

        msg += b'67gfd'  # Add random bytes to the message

    # Adds 2 valid commands
    for j in range(2):

        # Start of a command
        msg.append(STX)  # STX byte
        msg.append(random.randint(0, 127))  # CMD
        l = 5 + 2*j
        msg.append(l)  # DataLen

        for el in range(l):
            msg.append(random.randint(0, 255))  # D[i]

        # CRC byte is computed as a XOR of all the bytes in the message
        crc = STX
        for i in msg[-(l + 2):]:
            crc ^= i
        msg.append(crc)
        # End of a command

    # Add 1 half-complete command surrounded with random bytes to the message
    # Start of a command
    msg.append(STX)  # STX byte
    msg.append(random.randint(0, 127))  # CMD
    l = 4
    msg.append(l)  # DataLen
    msg.append(80)  # D[1]
    # The command lacks 3 additional data byte and 1 crc byte

    return msg



'''
Function: messageToBinaryFile
Inputs: fileName
Outputs:

Calls generateMessage() to generate a message.
Writes the message to a binary file - fileName.
'''
def messageToBinaryFile(fileName):

    msg = generateMessage()  # Generate the message

    # Try's to write the message to the binary file
    try:
        fh = open(fileName, 'wb')

    except IOError:
        print("Couldn't open ", fileName, " in wb mode.")

    else:
        fh.write(msg)
        fh.close()



def main():

    fileName = 'message.bin'  # File path of the binary file, where the message will be stored

    messageToBinaryFile(fileName)  # Generate a message and write it to a binary file



if __name__ == "__main__":
    main()
