'''
z3-serial-port.py
'''

import struct
import serial
import threading
import time
import generateTestMessage

STX = 2

'''
Function: process
Input: byte, buffer

Message by bytes:
STX - start signal
CMD - command signal
DataLen - length of the message
D[0] - first data byte
.
.
.
D[DataLen - 1] - last data byte
CRC - bytewise xor from STX to D[DataLen - 1]

If byte STX arrives on an empty buffer, it is added to the buffer.
Bytes are added until the byte at CRC's expected position arrives.
If the byte at the expected CRC position matches the computed CRC from the message, output the message.
Output an error otherwise.
'''
def process(byte, buffer):


    b = struct.pack('B', byte)

    if buffer.__len__() == 0:

        # Signal for the start of a command has arrived
        if byte == STX:
            buffer.append(byte)

        else:
            print("STX expected, ", struct.pack('B', byte), ' showed up.')
            print()

    # There is something in the buffer
    else:

        # The CRC byte has arrived
        if buffer.__len__() >= 3 and buffer.__len__() == (buffer[2]+3):

            buffer.append(byte)  # Add the received CRC byte to the buffer

            crc = buffer[0]

            # CRC = STX xor CMD xor ..... xor D[DataLen - 1]
            for el in buffer[1:-1]:

                crc ^= el

            # No errors in transmission
            if crc == buffer[-1]:

                msg = ''

                for el in buffer[3:-1]:
                    msg += str(el) + ' '  # Concatenate all the D[i] bytes

                # Print the message
                print("Command", buffer[1], "found -> printing command data: ")
                print(msg, "(Message length:", buffer[2], ")")
                print()

                buffer.clear()

            # Error in transmission
            else:
                # Print the error
                print("Error in transmission [CRC check not valid]")
                print()
                buffer.clear()
        
        # The command isn't at it's end yet
        else:
            buffer.append(byte)



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

        #time.sleep(0.05)

    port.close()  # Close the port



'''
Function: receive
Inputs: port
Outputs:

The function receives the Serial object - port.
The function reads bytes from the port and processes them one by one using the function process.
'''
def receive(port):

    buffer = bytearray()  # Create a empty buffer

    while True:

        b = port.read()  # Reads one byte from the port

        if b == b'':
            break

        b = struct.unpack('B', b)[0]  # Unpack the byte into an unsigned int

        process(b, buffer)  # Process the received byte

    port.close()



def main():

    com100 = serial.Serial('COM100')  # Open the COM100 serial port for sending the message

    com101 = serial.Serial('COM101', timeout=5)  # Opens the COM101 serial port for reading the incoming message,
                                                 # timeout is 5 sec

    th1 = threading.Thread(target=send, args=(com100,))

    th2 = threading.Thread(target=receive, args=(com101,))

    th1.start()

    th2.start()



if __name__ == "__main__":
    main()