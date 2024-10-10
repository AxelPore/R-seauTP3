from os import system
from sys import argv
from ipaddress import IPv4Address


ip = f"{argv[1]}"
try:    
    IPv4Address(ip)
    response = system(f"ping {argv[1]} > $null")

    if response == 0 :
        print(f"UP!")
    
    else :
        print(f"DOWN!")
except ValueError:
    print(ip, "is not a correct IPv4 address")


    
