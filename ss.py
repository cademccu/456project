import sys
import re as regex
import socket
import random
import threading
import struct
import sys
import os
import random



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

#FILE NAME PARSER, Modified from GetHowStuff
def parseFN(url):
    return url[url.rfind("/")+1:len(url)]


def relayFile(c,fn):

    file = open(fn,'rb')
    reading = file.read(1024)
    while reading:
        c.send(reading)
        reading = file.read(1024)

    file.close()
    c.shutdown(socket.SHUT_WR)
    c.close()



#When a thread has been created, immediately runs here
def threadedConnection(connection, address,ip):

    count, url, pairs = decode_data(connection.recv(1024))
    print("\tRequest: ",url)

    pairs.remove([ip,PORT])

    for pair in pairs:
        print("\t"+pair[0]+", "+pair[1])

    filename = parseFN(url)

    #LAST FILE IN CHAINGANG
    if count == 1:
        print("\tchainlist is empty")
        print("\tissuing wget for file "+url+"\n..")
        os.system("wget "+url+" >/dev/null 2>&1")

    #OTHERWISE, REMOVE THIS SS and CONTIUE TO NEXT SS
    else:
        count-=1

        randSS = random.choice(pairs)
        print("\tnext SS is "+randSS[0]+", "+randSS[1]+"\n\twaiting for file...\n..")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as nextSS:
            try:
                nextSS.connect((randSS[0],int(randSS[1])))
            except:
                print("Connection Refused")
                sys.exit()

            encodedData = encode_chains(count,url,pairs)

            nextSS.send(encodedData)

            #NOW WAIT FOR RECIEVED FILE

            ###TODO
            ###
            ###


            print("File received")
        nextSS.close()


    print("Relaying File ...")
    relayFile(connection,filename)
    print("Goodbye!")


# Main method
def main():
    setup()

    print("ss {}, {}".format(socket.gethostbyname(socket.gethostname()), PORT))

    ip = socket.gethostbyname(socket.gethostname())
    # TIME DO DO SOME SOCKET PROGRAMMING HELL YEEEE
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind to the host name and port
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((ip, int(PORT)))
    # set socket into listen mode
    listen_socket.listen(1)
    # create while loop to wait around for connection
    while 1:
        c, addy = listen_socket.accept()

        try:
            t = threading.Thread(target = threadedConnection, args = (c,addy[0],ip))
            t.start()
            t.join()
        except:
            print("Threading Error")


    # close socket
    listen_socket.close()


# Call to main method
if __name__ == "__main__":
    main()
