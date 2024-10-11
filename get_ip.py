from psutil import net_if_addrs
from socket import AddressFamily
from pprint import pprint

card = "Wi-Fi"

cidr = 0
dic = net_if_addrs()
addr, netm = None, None
for key, value in dic.items():
    if key == card:
        for i in range(len(value)):
            if value[i].family == AddressFamily.AF_INET:
                addr = value[i].address
                netm = value[i].netmask                
                for i in range(4) :
                    x = bin(int(netm.split(".")[i])).split("b")[1]
                    for j in x :
                        if j == "1" :
                            cidr += 1
print(addr + "/" + str(cidr))
print(2**(32-cidr))        