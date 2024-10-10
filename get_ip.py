from psutil import net_if_addrs

cidr = 0
dic = net_if_addrs()
for key, value in dic.items():
    if key == "Wi-Fi":
        addr = str(value[1]).split(", ")[1].split("=")[1].split("'")[1]
        netm = str(value[1]).split(", ")[2].split("=")[1].split("'")[1]
        for i in range(4) :
            x = bin(int(netm.split(".")[i])).split("b")[1]
            for j in x :
                if j == "1" :
                    cidr += 1
print(addr + "/" + str(cidr))
print(2**(32-cidr))        