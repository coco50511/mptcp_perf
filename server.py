import socket
import sys

import appconf

def start_tcp_server(ip, port):
	#create socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (ip, port)

	#bind port
	print 'starting listen on ip %s, port %s'%server_address
	sock.bind(server_address)

	#starting listening, allow only one connection
	try:
		sock.listen(1)
	except socket.error, e:
		print "fail to listen on port %s"%e
		sys.exit(1)

	while True:
		print "waiting for connection"
		client,addr = sock.accept()
		print 'having a connection'

		total_len = 0;
		while True:
			recv_data = client.recv(appconf.KBYTE)
			if not recv_data:
				break
			total_len = total_len + len(recv_data)

		client.close()
		print "received bytes: " + appconf.humanbytes(total_len) + "(" + str(total_len) + ")"

if __name__ == '__main__':
	start_tcp_server(appconf.server_ip, appconf.server_port)

