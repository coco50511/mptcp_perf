from subprocess import Popen, PIPE

# IP address and port number of server
server_ip = "10.70.5.58"
server_port = 5000

#  it is possible to create multiple subflows for each pair of IP-addresses.
num_subflows = 2
num_subflows_path = "/sys/module/mptcp_fullmesh/parameters/num_subflows"

# At run-time you can select one of the compiled schedulers
# 'default': This scheduler is the default one. It will first send data on subflows with the lowest RTT
#			until their congestion-window is full. Then, it will start transmitting on the subflows with 
#			the next higher RTT.
# 'redundant': This scheduler will try to transmit the traffic on all available subflows in a redundant way.
#			It is useful when one wants to achieve the lowest possible latency by sacrificing the bandwidth.
scheduler_value = "redundant"
scheduler_key = "net.mptcp.mptcp_scheduler"

# If you do not select a path-manager, the host will not trigger the creation of new subflows, nor advertise 
# alternative IP-addresses through the ADD_ADDR-option.
# 'default': This path-manager actually does not do anything. The host won't announce different IP-addresses
#			nor initiate the creation of new subflows. However, it will accept the passive creation of new subflows.
# 'fullmesh': It will create a full-mesh of subflows among all available subflows. Since v0.90 it is possible to
#			create multiple subflows for each pair of IP-addresses.
#			Just set /sys/module/mptcp_fullmesh/parameters/num_subflows to a value > 1.
#			If you want to re-create subflows after a timeout (e.g., if the NAT-mapping was lost due to idle-time),
#			you can set /sys/module/mptcp_fullmesh/parameters/create_on_err to 1.
# 'ndiffports': This one will create X subflows across the same pair of IP-addresses, modifying the source-port.
#			To control the number of subflows (X), you can set the sysfs /sys/module/mptcp_ndiffports/parameters/num_subflows to a value > 1.
# 'binder': The path-manager using Loose Source Routing from the paper Binder: a system to aggregate multiple internet gateways
#			in community networks.
pathman_value = "fullmesh"
pathman_key = "net.mptcp.mptcp_path_manager"

# Disable/Enable MPTCP on this machine. Possible values are 0 or 1. (default 1)
enable_value = 1
enable_key = "net.mptcp.mptcp_enabled"

# This file must be 1KB size.
send_data = "data.bin"
KBYTE = 1024


def setMptcp():
#	sysCtl(enable_key, str(enable_value))
#	sysCtl(pathman_key, pathman_value)
	writeFile(num_subflows_path, str(num_subflows))
	sysCtl(scheduler_key, scheduler_value)


def writeFile(path, data):
	fo = open(path, "w")
	print "write " + data + " to " + path
	fo.write(data)
	fo.close()


def sysCtl(key, value):
  p = Popen("sysctl -w %s=%s" % (key, value), shell=True, stdout=PIPE, stderr=PIPE)
  stdout, stderr = p.communicate()
  print "stdout=",stdout,"stderr=", stderr


def humanbytes(B):
   'Return the given bytes as a human friendly KB, MB, GB, or TB string'
   B = float(B)
   KB = float(KBYTE)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)


def kbytes(humanstr):
	sizestr, unit = splitSizestr(humanstr)
	size = int(sizestr)

	if unit == "G" :
		size = size * (KBYTE ** 2)
	elif unit == "M" :
		size = size * (KBYTE)

	return size

def splitSizestr(humanstr):
	upperHumanstr = humanstr.upper()
	sizestr = ""
	unit = ""

	for c in humanstr:
		if c.isdigit():
			sizestr = sizestr + c
		else:
			unit = c
			break;

	return sizestr, unit

