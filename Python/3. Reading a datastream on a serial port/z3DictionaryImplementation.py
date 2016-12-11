'''
z3-serial-port.py
'''

import serial
import threading
import generateTestMessage
import struct
import time

STX = 2

'''
Function: emptyCmd
Inputs:
Outputs: cmd

Generates a default command[dictionary] and outputs it.
A default command is used as a sign that no new commands have been received, nor they are being processed.
'''
def emptyCmd():
    cmd = {
            "stx": False,
            "cmd": -1,
            "len": -1,
            "data": bytearray(),
            "crc": -1
        }

    return cmd



'''
Function: process
Inputs: byte, cmd
Outputs:

Processes the received byte.
If an incoming command is noticed, starts writing it to - cmd.
When the whole command comes to an end, it is displayed on the command line if there are no transfer errors.
'''
def process(byte, cmd):

    # Start of the command (STX byte received)
    if byte == STX and cmd["stx"] is False:

        cmd["stx"] = True

    # 2nd [CMD] byte received
    elif cmd["stx"] is True and cmd["cmd"] == -1:

        cmd["cmd"] = byte
        cmd["crc"] = STX ^ byte

    # 3rd [DataLen] byte received
    elif cmd["cmd"] != -1 and cmd["len"] == -1:

        cmd["len"] = byte
        cmd["crc"] ^= byte

    # Data [D[i]] byte received
    elif cmd["len"] != -1 and len(cmd["data"]) < cmd["len"]:

        cmd["data"].append(byte)
        cmd["crc"] ^= byte

    # Last [CRC] byte received
    elif len(cmd["data"]) == cmd["len"]:

        # No errors in transmission
        if cmd["crc"] == byte:

            msg = ''
            for el in cmd["data"]:
                msg += str(el) + ' '  # Concatenate all the D[i] bytes

            # Print the command
            print("Command", cmd["cmd"], "found -> printing command data: ")
            print(msg, "(Message length:", cmd["len"], ")")
            print()

        # Error in transmission
        else:

            # Print the error
            print("There has been an error while trying to receive a message.")
            print()

        # Reset the cmd to default values
        cmd["stx"] = False
        cmd["cmd"] = -1
        cmd["len"] = -1
        cmd["data"] = bytearray()
        cmd["crc"] = -1


'''
Function: send
Inputs: port
Outputs:

The function receives the Serial object - port , on which to send the message.
The function generates the message [bytearray].
Finally, the function outputs the message on the port.
'''
def send(port):

    messageBytes = generateTestMessage.generateMessage()  # Generate the message, which is to be sent on the port

    # Output the message on the port, byte by byte
    for b in messageBytes:

        b = struct.pack('B', b)  # Convert b to byte

        port.write(b)  # Write b on the port

        time.sleep(0.05)

    port.close()  # Close the port



'''
Function: receive
Inputs: port
Outputs:

The function receives the Serial object - port.
The function reads bytes from the port and processes them one by one using the function process.
'''
def receive(port):

    cmd = emptyCmd()  # Create a default command

    while True:

        b = port.read()  # Reads one byte from the port

        if b == b'':     #b == b''
            break

        b = struct.unpack('B', b)[0]  # Unpack the byte into an unsigned int

        process(b, cmd)  # Process the received byte

    port.close()


def main():

    com100 = serial.Serial('COM100')  # Open the COM100 serial port for sending the message

    com101 = serial.Serial('COM101', timeout=5)  # Opens the COM101 serial port for reading the incoming message, timeout is 5 sec

    th1 = threading.Thread(target=send, args=(com100,))

    th2 = threading.Thread(target=receive, args=(com101,))

    th1.start()

    th2.start()



if __name__ == "__main__":
    main()
