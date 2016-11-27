import getopt, sys
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:r")

    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    file=''
    mode=''
    for o,a in opts:
        if o=='-i':
            file=a
        elif o=="-r":
            mode=o

    try:
        if mode == '-r':
            fh=open(file,'r')
            print(fh.read())
        elif mode == '-w':
            fh=open(file,'w')

    except IOError:
        print("The file doesnt exist")


if __name__ == "__main__":
    main()