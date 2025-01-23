import configparser
import sys
import os
import json
import requests
from aggregate_prefixes import aggregate_prefixes
from ipaddress import IPv4Address, IPv4Network, summarize_address_range


''' 
Script for download and set 'AllowedIPs' options in Wireguard config 
List IPs download from https://stat.ripe.net/ by specified country code
'''


def ip_country_ripe(country_code):
    filepath = os.path.dirname(os.path.abspath(sys.argv[0]))
    result = filepath + '/ip_' + country_code + '.lst'
    if not os.path.exists(result):
        networks = []
        url = 'https://stat.ripe.net/data/country-resource-list/data.json?resource='+country_code
        response = requests.get(url)
        if not response.ok:
            response.raise_for_status()

        try:
            ripe_ip = json.loads(response.content)[
                'data']['resources']['ipv4']
        except:
            raise

        with open(result, 'w', encoding='utf-8') as out_file:
            for record in ripe_ip:
                try:
                    if record.find('-') > -1:
                        ips = record.split('-')
                        ipaddr = list(summarize_address_range(
                            IPv4Address(ips[0]), IPv4Address(ips[1])))
                    else:
                        ipaddr = [IPv4Network(record)]
                    networks.extend(ipaddr)
                except:
                    raise
            for line in list(aggregate_prefixes(networks)):
                out_file.write(f"{str(line)}\n")
                yield str(line).strip()
    else:
        with open(result, 'r', encoding='utf-8') as in_file:
            for line in in_file:
                yield str(line).strip()


def add_to_config(allowed_ip_iter, configpath):
    allowed_ips = []
    section_peer = 'Peer'
    option_allowed_ips = 'AllowedIPs'
    config = configparser.ConfigParser()
    config.optionxform = str  # case-sensivity
    config_filename = ''

    if not os.path.exists(configpath):
        raise FileNotFoundError(f"{configpath} not exists!")
    with open(configpath, 'r', encoding='utf-8') as config_file:
        config_filename = config_file.name
        config.read_file(config_file)
        if not config.has_section(section_peer):
            raise configparser.NoSectionError(section_peer)
        if not config.has_option(section_peer, option_allowed_ips):
            raise configparser.NoOptionError(option_allowed_ips, section_peer)

    with open(f"{config_filename}.new", 'a', encoding='utf-8') as config_file:
        for ip in allowed_ip_iter:
            allowed_ips.append(ip)
        config.set(section_peer, option_allowed_ips, ", ".join(allowed_ips))
        config.write(config_file)
        print(f"Write to {config_file.name} complete")


if __name__ == "__main__":
    try:
        country_code = sys.argv[1].upper()
        config_file = sys.argv[2]
        add_to_config(ip_country_ripe(country_code), config_file)
    except IndexError:
        print('Usage: ', sys.argv[0],
              ' <country code (ie. RU)> <WG config file (*.conf)>')
    except Exception as ex:
        print(ex)
    finally:
        exit()
