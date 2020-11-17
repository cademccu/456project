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


# This takes the payload of the packet that contains
# the remaining chain list and decodes it into count
# and list of values repectively. If count is zero,
# returns None for pairs.
# @returns count, pairs
def decode_data(data):
    # the first 2 bytes are the count
    count = struct.unpack("h", data[:2])[0]

    # check if count is 0, if so no more data!
    if count == 0:
        return 0, None

    # unpack the rest into a string
    raw_string = data[2:].decode("utf-8")

    # split into list. Omit last value, empty element, My encoding adds additional '|'
    raw_values = raw_string.split("|")
    raw_values.pop()

    # sanity check
    if len(raw_values) != count:
        print("Something went wrong!")
        print("count:      ", count)
        print("raw_values: ", raw_values)

    # create list of pairs from data
    pairs = []
    for pair in raw_values:
        pairs.append(pair.split(","))

    return count, pairs


#When a thread has been created, immediately runs here
def threadedConnection(connection, address):
    print(connnection, address)

    count, pairs = decode_data(connection.recieve(1024))
    print(count, pairs)

    #LAST FILE IN CHAINGANG
    if count == 0:
        os.system("wget")




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
