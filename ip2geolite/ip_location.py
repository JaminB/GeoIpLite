import json
import sqlite3
import pkgutil
from os import path
from sys import stderr
from requests import get
from random import randint
from datetime import datetime

DB_PATH = 'ip2geo.db'
MAPPINGS_PATH = 'mappings/'

CREATE_LOCATION_TABLE = '''
    CREATE TABLE ip_locations (
        ctime DATETIME,
        ip text,
        asn text,
        cc text,
        city text,
        country text,
        dns_name text,
        isp text,
        latitude float,
        longitude float,
        org text,
        postal text,
        rc text,
        region text
    );
'''

CREATE_LOCATION_TABLE_INDEX = '''
    CREATE INDEX ip_index ON ip_locations (ip);
'''

DROP_LOCATION_TABLE = '''
    DROP TABLE IF EXISTS ip_locations;
'''

INSERT_LOCATION = '''
    INSERT INTO ip_locations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);
'''

SELECT_LOCATION_BY_IP = """
    SELECT * FROM ip_locations WHERE ip='{}';
"""


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_database(overwrite=True):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if overwrite:
        c.execute(DROP_LOCATION_TABLE)
    c.execute(CREATE_LOCATION_TABLE)
    c.execute(CREATE_LOCATION_TABLE_INDEX)
    conn.close()


class IPLookup:

    def __init__(self, ip):
        self.ip = ip
        self.asn = None
        self.cc = None
        self.city = None
        self.country = None
        self.dns_name = None
        self.isp = None
        self.latitude = None
        self.longitude = None
        self.org = None
        self.rc = None
        self.region = None
        self.postal = None
        self.fetch()

    def __str__(self):
        return json.dumps(dict(
            ip=self.ip,
            asn=self.asn,
            cc=self.cc,
            city=self.city,
            country=self.country,
            dns_name=self.dns_name,
            isp=self.isp,
            latitude=self.latitude,
            longitude=self.longitude,
            org=self.org,
            rc=self.rc,
            region=self.region,
            postal=self.postal
        ), indent=2)

    def _get_random_lookup_api(self):
        """
        :return: Returns url and mappings for a random ip2geo API
        """
        paths = [
            'mappings/api.petabyet.json',
            'mappings/extreme-ip-lookup.json',
            'mappings/ip-api.json',
            'mappings/ipapi.json'
        ]
        lookup_apis = []
        for p in paths:
            try:
                mapping = json.loads(pkgutil.get_data('ip2geolite', p).decode('utf-8'))
            except:
                mapping = json.loads(open(p, 'r').read())
            if mapping['switch_param_and_endpoint']:
                url = path.join(mapping['host'], self.ip, mapping['endpoint'])
            else:
                url = path.join(mapping['host'], mapping['endpoint'], self.ip)
            fields = mapping['fields']
            lookup_apis.append((url, fields))
        return lookup_apis[randint(0, len(lookup_apis) - 1)]

    def cache(self):
        """
        Stores the results of a query to our local database for a quick fetch
        """
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        res = [datetime.utcnow(),
               self.ip,
               self.asn,
               self.cc,
               self.city,
               self.country,
               self.dns_name,
               self.isp,
               self.latitude,
               self.longitude,
               self.org,
               self.rc,
               self.region,
               self.postal
               ]
        c.execute(INSERT_LOCATION, res)
        conn.commit()
        conn.close()

    def fetch(self, attempts=8):
        """
        :param attempts: Number of attempts against various APIs before giving up
        :return: True if fetch was successful
        """
        in_cache = self.fetch_from_cache()
        if in_cache:
            return True
        url, m_fields = self._get_random_lookup_api()
        try:
            res = get(url)
            if res.status_code == 200:
                content = res.json()
                for field in content:
                    n_field = m_fields.get(field)
                    value = content[field]
                    if n_field is None:
                        continue
                    if str(value).lower().strip() == 'null' or str(value).lower().strip() == '':
                        continue
                    if n_field == "latitude" or n_field == "longitude":
                        try:
                            value = float(content[field])
                        except ValueError:
                            value = None
                    setattr(self, n_field, value)
                if self.latitude is None or self.longitude is None:
                    if attempts == 0:
                        return False
                    self.fetch(attempts=attempts - 1)
                self.cache()
                return True
        except Exception as e:
            stderr.write(str(e) + '\n')
            if attempts == 0:
                self.fetch(attempts=attempts - 1)
            else:
                return False

    def fetch_from_cache(self):
        """
        :return: True if found in cache
        """
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.row_factory = _dict_factory
        res = c.execute(SELECT_LOCATION_BY_IP.format(self.ip))
        content = res.fetchone()
        if not content:
            return False
        for field in content:
            setattr(self, field, content[field])
        return True
