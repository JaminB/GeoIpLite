from setuptools import setup, find_packages

setup(
    name='GeoIpLite',
    version='0.5',
    url='https://packettotal.com',
    license='MIT',
    author='Jamin Becker',
    author_email='jamin@packettotal.com',
    description='Lightweight library for retrieving location information about Ipv4/Ipv6 addresses',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    package_data={'': ['mappings/*.json']},
    include_package_data=True,
    scripts=[
        'scripts/ip_lookup.py'
    ]
)
