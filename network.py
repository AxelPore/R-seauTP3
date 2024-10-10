from socket import gethostbyname
from sys import argv
from re import search
from os import *
from ipaddress import IPv4Address
from psutil import net_if_addrs
from datetime import *

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
    return ["[INFO]", f"{addr}/{cidr} \n{nbra}"]

def Cfolder():
    source = "%appdata%/Local/Temp"
    try:
        mkdir(source)
    except FileExistsError:
        pass
    except PermissionError:
        pass
    except Exception as e:
        pass
    source += "/network_tp3"
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
    match command:
        case "lookup":
            if r == "[ERROR]":
                z = 2
            else :
                z = 0
        case "ping" :
            if r == "[ERROR]":
                z = 2
            else :
                z = 0
        case "ip":
            z = 1
        case _ :
            z = 3
    return z
    
def log(r, command, arg, z):
    LOG_FILE = "%\appdata%/Local/Temp/network_tp3/network.log"
    today = date.today()
    now = datetime.now()
    atime = now.strftime("%H:%M:%S")
    if z == 0:
        LOG = f"{today} {atime} {r} Command {command} called successfully with argument {arg}."
    if z == 1:
        LOG = f"{today} {atime} {r} Command {command} called successfully."
    if z == 2:
        LOG = f"{today} {atime} {r} Command {command} called with bad arguments : {arg}."
    if z == 3:
        LOG = f"{today} {atime} {r} Invalid command : {command} doesnt exist"
    f = open(LOG_FILE, "a")
    f.write(LOG)
    f.close()
    return LOG_FILE

    
    
def main(): 
    Cfolder()
    p = None
    r = None
    match argv[1]:
        case "lookup":
            r, p = lookup(argv[2])
        case "ping" :
            r, p = ping(argv[2])
        case "ip":
            r, p = ip()
        case _ :
            p = f"{argv[1]} is not an available command."
            r = "[ERROR]"
    z = status(r, argv[1])
    if len(argv) == 2:
        t = None
    else :
        t = argv[2]
    LOG_FILE = log(r, argv[1], t, z)
    print(p)
    f = open(LOG_FILE, "r")
    print(f.read())
main()