Hi,
The folder contains two files : ktjosh_ping.py , ktjosh_traceroute.py


-------------------------------------------------------------------------------------------------------------------
===================================================================================================================

** Note 1: The files will not run on unix machines (RIT CS machines) as it needs sudo previliges
		   It will run on a windows  machine.

** Note 2: for some machines to run ktjosh_traceroute.py you will need to turn off the windows firewall as 
	       it may or may not allow the program to listen to packets sent by intermediate routers.
** Note 3: The program needs Python 3.4 or higher

==================================================================================================================
------------------------------------------------------------------------------------------------------------------

'ktjosh_ping.py' file sends icmp echo request to check the host reachability.

To run the file you will have to type the command ' Python ktjosh_ping.py host_name '
e.g. 'Python ktjosh_ping.py google.com' OR  'Python3 ktjosh_ping.py google.com'

It has differnt options 

-c count        : Stop after sending (and receiving) count ECHO_RESPONSE packets. 

-i wait         : Wait wait seconds between sending each packet. 

-s packetsize   : Specify the number of data bytes to be sent.

-t timeout      : Specify a timeout, in seconds, before ping exits regardless of how many packets have been received.

>>> To run the Ping program with options 
	Type : 'Python Python ktjosh_ping.py [-c count] [-i wait_time] [-s packetsize] [ -t timeout_value] host_name'
	
-------------------------------------------------------------------------------------------------------------------

'ktjosh_traceroute.py' file prints all the intermediate nodes the packet goes through to reach destination host.

To run the file you will need to type the command 'Python ktjosh_traceroute.py host_name'
e.g. 'Python ktjosh_traceroute.py google.com' OR  'python3 ktjosh_traceroute.py google.com'

IT has differnt options

-n 				:Print hop addresses numerically rather than symbolically and numerically.

-q nqueries 	:Set the number of probes per  'ttl' to nqueries.

-S				:Print a summary of how many probes were not answered for each hop.

>>> To run the Ping program with options 
	Type : 'Python ktjosh_traceroute.py [-n] [-q probes_count] [-S]  host_name' 
	
-------------------------------------------------------------------------------------------------------------------
Thank you.

	

