=== CS457 Project 2: Anonymous Web Get ===
Contributors: Cade McCumber, Steven Lamp
Created: 10/31/2020
Version: 0.1



=== Description ===
Anonymous web get project that uses stepping
stones to anonymously traverse a network.


=== Usage ===

AWGET:
python3 awget.py <FILE> -c <CHAINFILE>
	<FILE>      (required) - Is the url of the file, image, or webpage you wish to fetch.
	<CHAINFILE> (optional) - Specified with a -c AFTER providing the <FILE> argument, the chainfile is the list of <address, port> pairs. Defaults to chaingang.txt if not -c <CHAINFILE> is provided.
	*** Only provide the -c <CHAINFILE> after providing the required <FILE> argument.
	*** Run awget.py in the same directory as the default chainfile if using default. If not, the path tp the chainfile must be from the working directory awget.py is being run in.

SS: Default Port is 20000
python3 ss.py -p <PORT>
	<PORT> (optional) - Specified with -p. Give a port number in the accepted range of ports (0-65535) to use. Defaults to port 20000 if no port is specifed.
	*** Run each instance of ss.py in seperate directories if running from a shared directory (such as multiple computers from the same account on the CSU CS lab machines). If running each instance from different accounts on different computers, this is optional.

