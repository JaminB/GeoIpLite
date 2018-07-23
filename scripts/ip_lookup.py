from ip2geolite import ip_location
from os import listdir
from sys import argv


if __name__ == '__main__':
    if 'ip2geo.db' not in listdir('.'):
        ip_location.create_database()
    for arg in argv[1:]:
        print(ip_location.IPLookup(str(arg).strip()))
