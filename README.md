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

## Output
```
{
  "org": null,
  "city": null,
  "country": "United States",
  "dns_name": "alu7750testscr.xyz1.gblx.mgmt.level3.net",
  "ip": "4.4.4.4",
  "rc": "New York",
  "region": null,
  "cc": "US",
  "postal": null,
  "asn": null,
  "isp": null,
  "latitude": 40.7111,
  "longitude": -73.9469
}
{
  "org": null,
  "city": "Mountain View",
  "country": "United States",
  "dns_name": null,
  "ip": "8.8.8.8",
  "rc": "California",
  "region": "94043",
  "cc": "US",
  "postal": "CA",
  "asn": "AS15169 Google LLC",
  "isp": null,
  "latitude": 37.4229,
  "longitude": -122.085
}
```


