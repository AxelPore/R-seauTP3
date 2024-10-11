from socket import gethostbyname, AddressFamily
from sys import argv
from re import search
from os import system, mkdir
from ipaddress import IPv4Address
from psutil import net_if_addrs
from datetime import date, datetime
import platform

def lookup(domn):
    reg = r"^(?=.{4,255}$)([a-zA-Z0-9][a-zA-Z0-9-]{,61}[a-zA-Z0-9]\.)+[a-zA-Z0-9]{2,5}$"

    if search(reg, domn):
        return ["[INFO]", gethostbyname(domn)]
    else :
        return ["[ERROR]", f"{domn} is not a valid domain name"]
        
def ping(ipa):
    ip = f"{ipa}"
    try:    
        IPv4Address(ip)
        response = system(f"ping {ipa} > $null")

        if response == 0 :
            return ["[INFO]", f"UP!"]
        
        else :
            return ["[INFO]", "DOWN!"]
    except ValueError:
        return ["[ERROR]", f"{ip} is not a correct IPv4 address"]
        
def ip(os):
    rcard = None
    if os == "Windows":
        rcard = "Wi-Fi"
    elif os == "Linux":
        rcard = "enp0s8"
    else:
        exit
    cidr = 0
    dic = net_if_addrs()
    addr, netm = None, None
    for key, value in dic.items():
        if key == rcard:
            for i in range(len(value)):
                if value[i].family == AddressFamily.AF_INET:
                    addr = value[i].address
                    netm = value[i].netmask                
                    for i in range(4) :
                        x = bin(int(netm.split(".")[i])).split("b")[1]
                        for j in x :
                            if j == "1" :
                                cidr += 1
    nbra = 2**(32-cidr)
    return ["[INFO]", f"{addr}/{cidr} \n{nbra}"]

def Cfolder(os):
    if os == "Windows":
        source = r"C:\Users\axelp\AppData\Local\Temp"
    elif os == "Linux":
        source = "/tmp"
    else:
        exit
    try:
        mkdir(source)
    except FileExistsError:
        pass
    except PermissionError:
        pass
    except Exception as e:
        pass
    if os == "Windows":
        source += r"\network_tp3"
    elif os == "Linux":
        source = "\network_tp3"
    else:
        exit
    try:
        mkdir(source)
    except FileExistsError:
        pass
    except PermissionError:
        pass
    except Exception as e:
        pass
    
def status(r, command):
    z = None
    if command == "lookup":
        if r == "[ERROR]":
            z = 2
        else :
            z = 0
    elif command == "ping" :
        if r == "[ERROR]":
            z = 2
        else :
            z = 0
    elif command == "ip":
        z = 1
    else :
        z = 3
    return z
    
def log(r: str, command: str, arg: str, z: int, os):
    LOG_FILE = None
    if os == "Windows":
        LOG_FILE = r"C:\Users\axelp\AppData\Local\Temp\network_tp3\network.log"
    elif os == "Linux":
        LOG_FILE = "/tmp/network_tp3/network.log"
    else:
        exit   
    today = date.today()
    now = datetime.now()
    atime = now.strftime("%H:%M:%S")
    if z == 0:
        LOG = f"{today} {atime} {r} Command {command} called successfully with argument {arg}. \n"
    if z == 1:
        LOG = f"{today} {atime} {r} Command {command} called successfully. \n"
    if z == 2:
        LOG = f"{today} {atime} {r} Command {command} called with bad arguments : {arg}. \n"
    if z == 3:
        LOG = f"{today} {atime} {r} Invalid command : {command} doesnt exist \n"
    f = open(LOG_FILE, "a")
    f.write(LOG)
    f.close()

def Osdefine():
    os = 0
    if platform.system() == "Windows":
        os = 1
    elif platform.system() == "Linux":
        os = 2
    else :
        pass
    return os
    
def main(): 
    os = Osdefine()
    Cfolder(os)
    p = None
    r = None
    if argv[1] == "lookup":
        r, p = lookup(argv[2])
    elif argv[1] == "ping" :
        r, p = ping(argv[2])
    elif argv[1] == "ip":
        r, p = ip(os)
    else :
        p = f"{argv[1]} is not an available command."
        r = "[ERROR]"
    z = status(r, argv[1])
    if len(argv) == 2:
        t = None
    else :
        t = argv[2]
    log(r, argv[1], t, z, os)
    print(p)
main()