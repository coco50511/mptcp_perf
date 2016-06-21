[Description]
 This python script measure the bandwidth on multi path TCP.

[install MPTCP]
 sudo apt-get update
 sudo apt-get install linux-mptcp

[Booting from linux kernel patched MPTCP]

[Configure MPTCP]
 At appconf.py, you could change the configuration such as server ip address, port number and mptcp parameters
 About MPTCP has been descripted in more detailed at http://multipath-tcp.org/pmwiki.php/Users/ConfigureMPTCP

[Run]
- Server
 python2 server.py
- Client
 sudo python2 client.py -s 2G
