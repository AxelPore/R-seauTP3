from socket import gethostbyname
from sys import argv
from re import search
from os import system
from ipaddress import IPv4Address
from psutil import net_if_addrs

def lookup(domn):
    reg = r"^(?=.{4,255}$)([a-zA-Z0-9][a-zA-Z0-9-]{,61}[a-zA-Z0-9]\.)+[a-zA-Z0-9]{2,5}$"

    if search(reg, domn):
        return gethostbyname(domn)
    else :
        return f"{domn} is not a valid domain name"
        
def ping(ipa):
    ip = f"{ipa}"
    try:    
        IPv4Address(ip)
        response = system(f"ping {ipa} > $null")

        if response == 0 :
            return f"UP!"
        
        else :
            return "DOWN!"
    except ValueError:
        return f"{ip} is not a correct IPv4 address"
        
def ip():
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
    nbra = 2**(32-cidr)
    return f"{addr}/{cidr} \n{nbra}"
        
    
def main(): 
    p = None
    match argv[1]:
        case "lookup":
            p = lookup(argv[2])
        case "ping" :
            p = ping(argv[2])
        case "ip":
            p = ip()
        case _ :
            p = f"{argv[1]} is not an available command."
    print(p)
main()