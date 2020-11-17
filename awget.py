import sys
import random
import socket
import struct


# processes chain file into object for use
class Chains:
    def __init__(self, chains):
        flist = list(chains)
        self.num_entries = int(flist[0])
        self.entries = []
        for i in range(self.num_entries):
            self.entries.append(flist[i+1].split())
            # file should follow constant format so we can not care





# get command line url, check number of params, etc
def setup():
    global URL, chainfilename
    if len(sys.argv) == 1:
        print("\nUSAGE\n\tpython3 reader.py <ARG> -c <CHAINFILE>\n\t\t<ARG> - URL of the file you wish to retrieve.\n\t\t<CHAINFILE> - (Optional) the name of the file ",
            "containing the chain you wish to use.\n")
        sys.exit()

    URL = sys.argv[1]
    chainfilename = "chaingang.txt" # default

    if len(sys.argv) == 2:
        return

    if sys.argv[2] == "-c":
        if len(sys.argv) != 4:
            print("\nUSAGE\n\tpython3 reader.py <ARG> -c <CHAINFILE>\n\t\t<ARG> - URL of the file you wish to retrieve.\n\t\t<CHAINFILE> - (Optional) the name of the file ",
            "containing the chain you wish to use.\n")
            sys.exit()
        chainfilename = sys.argv[3]
    return

# This takes the chain object read from the chains file,
# and encodes it into a binary 'packet' to be transmitted
# The 'packet' can then be unpacked by using '.decode' on
# this part of the actual packet, reading the count into
# a python integer, and through 2 series of '.split'
# retrieve the rest of the list. The last item of the 
# unoacked list will be the URL
def encode_chains(chains):
    # pack the count of <address, port> pairs
    b_count = struct.pack("h", int(chains.num_entries))

    b_string = ""
    for s in chains.entries:
        b_string = b_string + s[0] + "," + s[1] + "|"

    # encode to bytes
    b_string = b_string.encode("utf-8")

    # add url as last member of the list
    return b_count + b_string + URL.encode("utf-8")
    # not_needed_but_example = struct.pack(str(len(b_string)) + "s", b_string)

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
        print("raw_values: ", raw_values)

    # create list of pairs from data
    pairs = []
    for pair in raw_values:
        pairs.append(pair.split(","))

    return count, url, pairs


# Main method
def main():

    setup()

    try:
        chains_file = open(chainfilename, "r")
    except FileNotFoundError:
        print("\nThe chainfile [ ", chainfilename, " ] could not be opened. Exiting...\n")
        sys.exit()

    # chain file object
    chains = Chains(chains_file)

    # get binary representation of chains file
    b_chains = encode_chains(chains)

    print(b_chains)
    count, pairs, url = decode_data(b_chains)
    print(count)
    print(pairs)
    print(url)

    # output section
    print("awget:")
    print("\tRequest: ", URL)
    print("\tchainlist is")
    for pair in chains.entries:
        print("\t{}, {}".format(pair[0],pair[1]))

    # get a random number in the apropriate range
    pair_index = random.randrange(len(chains.entries))
    pair = chains.entries[pair_index]

    # TIME DO DO SOME SOCKET PROGRAMMING HELL YEEEE
    out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind to the host name and port
    out_socket.bind((socket.gethostname(), int(pair[1])))
    # set socket into listen mode
    out_socket.listen(1)



    # close socket
    out_socket.close()





    if False: # debugging
        print("\n######### DEBUG #########")
        print("URL: ", URL)
        print("filename: ", chainfilename)
        print("Number of entries: ", chains.num_entries)
        print("entry list: ", chains.entries)


        print("#########################\n")


if __name__ == "__main__":
    main()
