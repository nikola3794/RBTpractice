
def emptyMsg():
    message = {
            "stx" : False,
            "cmd" : -1,
            "len":-1,
            "data" : bytearray(),
            "crc" : -1
        }

    return message

def process(data,message):
    for b in data:

        if b == 2 and message["stx"] == False:
            message["stx"] = True
            continue

        elif message["stx"] == True and message["cmd"] == -1:
            message["cmd"] = b
            message["crc"] = 2 ^ b
            continue

        elif message["cmd"] != -1 and message["len"] == -1:
            message["len"] = b
            message["crc"] ^= b
            continue

        elif message["len"] != -1 and len(message["data"]) < message["len"]:
            message["data"].append(b)
            message["crc"] ^= b
            continue

        elif len(message["data"]) == message["len"]:
            if message["crc"] == b:
                msg=''
                for el in message["data"]:
                    msg += str(el) + ' '

                print("Command", message["cmd"], "found -> printing command data: ")
                print(msg,"(Message length:",message["len"],")")

            else:
                print("There has been an error while trying to recieve a message.")

            message["stx"] = False
            message["cmd"] = -1
            message["len"] = -1
            message["data"] = bytearray()
            message["crc"] = -1


def main():

    try:
        fh=open('message.bin','rb')

    except IOError as e:
        print(e)

    else:
        data = fh.read(9)

        message = emptyMsg()

        while data != b'':
            process(data, message)

            data = fh.read(9)

        print("Terminated with message",message)
        fh.close()



if __name__ == "__main__":
    main()
