import sys
import random
import socket


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
