import sys
import re as regex
import socket
import random
import _thread
import struct
import sys
import os



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
# @returns count, url, pairs
def decode_data(data):
    # the first 2 bytes are the count
    count = struct.unpack("h", data[:2])[0]

    # check if count is 0, if so no more data!
    if count == 0:
        return 0, data[2:].decode("utf-8"), None

    # unpack the rest into a string
    raw_string = data[2:].decode("utf-8")

    # split into list. Omit last value, empty element, My encoding adds additional '|'
    raw_values = raw_string.split("|")
    url = raw_values.pop()

    # sanity check
    if len(raw_values) != count:
        print("Something went wrong!")
        print("count:      ", count)
        print("url:        ", url)
        print("raw_values: ", raw_values)

    # create list of pairs from data
    pairs = []
    for pair in raw_values:
        pairs.append(pair.split(","))

    return count, url, pairs

# This encodes the count, remaining chainlist (if any), and url to be gotten into
# a binary object.
# count - an integer count of number of pairs left in chainlist
# url - the name of the file or url to be fetched
# pairs - the list of lists of pairs remaining
# @returns a binary string containing the encoded data
def encode_chains(count, url, pairs=None):
    # pack the count of <address, port> pairs
    b_count = struct.pack("h", count)

    # if count is 0, don't encode list.
    if count == 0:
        return b_count + url.encode("utf-8")

    b_string = ""
    for s in pairs:
        b_string = b_string + s[0] + "," + s[1] + "|"

    # encode to bytes
    b_string = b_string.encode("utf-8")

    # add url as last member of the list
    return b_count + b_string + url.encode("utf-8")
    # not_needed_but_example = struct.pack(str(len(b_string)) + "s", b_string)





#When a thread has been created, immediately runs here
def threadedConnection(connection, address):

    count, url, pairs = decode_data(connection.recv(1024))
    print(count, ", ", url, ", ", pairs)



    #LAST FILE IN CHAINGANG
    if count == 1:
        os.system("wget "+url)

    else:
        count-=1






# Main method
def main():
    setup()

    print("ss {}, {}".format(socket.gethostbyname(socket.gethostname()), PORT))

    # TIME DO DO SOME SOCKET PROGRAMMING HELL YEEEE
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind to the host name and port
    listen_socket.bind((socket.gethostbyname(socket.gethostname()), int(PORT)))
    # set socket into listen mode
    listen_socket.listen(1)
    # create while loop to wait around for connection

    #while 1:
    c, addy = listen_socket.accept()

    test = c.recv(1024)
    print(test)

        try:
            _thread.start_new_thread(threadedConnection,(c,addy[0]))
        except:
            print("FUK")


    # close socket
    listen_socket.close()


# Call to main method
if __name__ == "__main__":
    main()
