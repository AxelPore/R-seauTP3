from socket import gethostbyname
from sys import argv
from re import search

reg = r"^(?=.{4,255}$)([a-zA-Z0-9][a-zA-Z0-9-]{,61}[a-zA-Z0-9]\.)+[a-zA-Z0-9]{2,5}$"

if search(reg, argv[1]):
    print(gethostbyname(argv[1]))
else :
    print(f"{argv[1]} is not a valid domain name")