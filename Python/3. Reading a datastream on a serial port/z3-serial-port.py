'''
z3-serial-port.py
'''

'''
Function: emptyCmd()
Inputs:
Outputs: cmd

Generates a default command and outputs it.
A default command is used as a sign that no new commands have been received nor they are being processer.
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
Function: process(buffer, cmd)
Inputs: buffer, cmd
Outputs:

Processes the bytes in the buffer.
If an incoming command is noticed, starts writing it to cmd.
When the whole command comes to an end, it is displayed on the command line if there are no transfer errors.
'''
def process(buffer, cmd):
    for b in buffer:

        if b == 2 and cmd["stx"] is False:
            # STX byte received
            cmd["stx"] = True
            continue

        elif cmd["stx"] is True and cmd["cmd"] == -1:
            # CMD byte received
            cmd["cmd"] = b
            cmd["crc"] = 2 ^ b
            continue

        elif cmd["cmd"] != -1 and cmd["len"] == -1:
            # DataLen byte received
            cmd["len"] = b
            cmd["crc"] ^= b
            continue

        elif cmd["len"] != -1 and len(cmd["data"]) < cmd["len"]:
            # D[i] byte received
            cmd["data"].append(b)
            cmd["crc"] ^= b
            continue

        elif len(cmd["data"]) == cmd["len"]:
            # CRC byte received

            if cmd["crc"] == b:
                # No error in transmission
                msg = ''
                for el in cmd["data"]:
                    msg += str(el) + ' '  # Concatenate all the D[i] bytes

                # Print the message
                print("Command", cmd["cmd"], "found -> printing command data: ")
                print(msg, "(Message length:", cmd["len"], ")")
                print()

            else:
                # Error in transmission

                # Print the error
                print("There has been an error while trying to receive a message.")
                print()

            # Reset the cmd to default values
            cmd["stx"] = False
            cmd["cmd"] = -1
            cmd["len"] = -1
            cmd["data"] = bytearray()
            cmd["crc"] = -1


def main():

    # Try's to read the message from the binary file
    try:
        fh = open('message.bin', 'rb')

    except IOError as e:
        print(e)

    else:
        buffer = fh.read(5)  # Load the buffer with 5 bytes
 
        cmd = emptyCmd()  # Generate an empty command

        while buffer != b'':  # While there are bytes to read

            process(buffer, cmd) # Process the bytes in the buffer

            buffer = fh.read(5)  # Load the buffer with 5 bytes

        print("Terminated with message at state:", cmd)
        fh.close()



if __name__ == "__main__":
    main()
