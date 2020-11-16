import sys
import re as regex
import socket
import random
import threading

def setup():
    global PORT
    if len(sys.argv) == 3:
        if sys.argv[1] != "-p":
            print("\nUSAGE\n\tpython3 ss.py -p <PORT>\n\t\t<PORT> - (Optional) Allowed port number.\n")
            sys.exit(-1)
        if regex.search("^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$", sys.argv[2]):
            PORT = sys.argv[2]
            return
        print("Port was outside of allowed port range. Exiting...")
        sys.exit(-1)
    elif len(sys.argv) == 1:
        PORT = 888
        return
    else:
        print("\nUSAGE\n\tpython3 ss.py -p <PORT>\n\t\t<PORT> - (Optional) Allowed port number.\n")
        sys.exit(-1)



def threadedConnection(connection, address):
    print(connnection, address)


# Main method
def main():
    setup()

    print("ss {}, {}".format(socket.gethostname(), PORT))

    # TIME DO DO SOME SOCKET PROGRAMMING HELL YEEEE
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind to the host name and port
    listen_socket.bind((socket.gethostname(), int(PORT)))
    # set socket into listen mode
    listen_socket.listen(1)
    # create while loop to wait around for connection

    while 1:
        c, addy = listen_socket.accept()

    try:
        thread.start_new_thread(threadedConnection,(c,addy))
    except:
        print("YOU DID SOMETIN WRONG BOI")


    # close socket
    listen_socket.close()


# Call to main method
if __name__ == "__main__":
    main()
