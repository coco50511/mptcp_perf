# Must be run as root.

import socket
import sys
import argparse
import time, datetime

import appconf

parser = argparse.ArgumentParser()
parser.add_argument('--transfer_size', '-s',
                    help='How many bytes to send. ex 1MB 10MB 100MB 500MB 1GB',
                    required=True,
					default='1MB',
                    action='store',
                    dest='transfer_size')

args = parser.parse_args()


def start_tcp_client(ip, port, size_as_kb):
	tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# connect to server
	try:
		tcp_client.connect((ip, port))
	except socket.error:
		print 'fail to setup socket connection'
		return

	# send data
	data = get_data(appconf.send_data)
	start_time = int(time.time())

	i = 0
	try:
		while i < size_as_kb:
			tcp_client.send(data)
			i = i + 1
	except socket.error:
		print 'fail to send data'

	sent_duration = int(time.time()) - start_time
	sent_size = i * appconf.KBYTE
	print "Transfered size: " + appconf.humanbytes(sent_size)
	if 0 < sent_duration:
		print "Transfered time: " + str(sent_duration) + "s"
		print "Transfered speed: " + appconf.humanbytes(sent_size / sent_duration) + "ps"
	else:
		print "Transfered time: less than 1s"

	# close connect
	tcp_client.close()


def get_data(filepath):
	fp = open(filepath,'rb')
	filedata = fp.read()
	fp.close()
	return filedata


if __name__ == '__main__':
	appconf.setMptcp()

	kb = appconf.kbytes(args.transfer_size)
	print "Start transfer: " + appconf.humanbytes(kb * appconf.KBYTE)

	start_tcp_client(appconf.server_ip, appconf.server_port, kb)

