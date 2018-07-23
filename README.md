## Description

GeoIpLite is yet another IP2Geo library that aims to make the process for looking up geographical information about IP addresses as simple as possible.

This library provides an alternative method for looking up IP addresses. Rather than rely on large local lookup files, this library relies on multiple free APIs, and round-robins requests to each, caching the results.

## Installation

```
git clone https://github.com/JaminB/GeoIpLite.git
python3 setup.py install
```

## Usage

```
from ip2geolite import ip_location

ip_location.create_database()
print(ip_location.IPLookup('8.8.8.8'))
```

## Scripts

```
scripts/ip_lookup.py 4.4.4.4 8.8.8.8
```




