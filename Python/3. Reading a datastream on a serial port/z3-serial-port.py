'''

'''
def emptyCmd():
    cmd = {
            "stx" : False,
            "cmd" : -1,
            "len":-1,
            "data" : bytearray(),
            "crc" : -1
        }

    return cmd

def process(buffer, cmd):
    for b in buffer:

        if b == 2 and cmd["stx"] == False:
            cmd["stx"] = True
            continue

        elif cmd["stx"] == True and cmd["cmd"] == -1:
            cmd["cmd"] = b
            cmd["crc"] = 2 ^ b
            continue

        elif cmd["cmd"] != -1 and cmd["len"] == -1:
            cmd["len"] = b
            cmd["crc"] ^= b
            continue

        elif cmd["len"] != -1 and len(cmd["data"]) < cmd["len"]:
            cmd["data"].append(b)
            cmd["crc"] ^= b
            continue

        elif len(cmd["data"]) == cmd["len"]:
            if cmd["crc"] == b:
                msg=''
                for el in cmd["data"]:
                    msg += str(el) + ' '

                print("Command", cmd["cmd"], "found -> printing command data: ")
                print(msg,"(Message length:", cmd["len"], ")")
                print()

            else:
                print("There has been an error while trying to recieve a message.")
                print()

            cmd["stx"] = False
            cmd["cmd"] = -1
            cmd["len"] = -1
            cmd["data"] = bytearray()
            cmd["crc"] = -1


def main():

    # Trys to read the message from the binary file
    try:
        fh=open('message.bin','rb')

    except IOError as e:
        print(e)

    else:
        buffer = fh.read(5) # Load the buffer with 5 bytes
 
        cmd = emptyCmd() # Generate an empty 

        while buffer != b'':
            process(buffer, cmd)

            buffer = fh.read(5)

        print("Terminated with message at state:",cmd)
        fh.close()



if __name__ == "__main__":
    main()
