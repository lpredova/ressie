import os
import re
import time

import requests

from ressie.configurations.config import Config


class IP(object):
    v_total_key = None
    tor_exits = "https://check.torproject.org/exit-addresses"
    tor_nodes = os.getcwd() + "/data/tor/exit-addresses"
    tor_ip = os.getcwd() + "/data/tor/exit-ip"

    def __init__(self):
        configuration = Config()
        self.v_total_key = configuration.parse_config("VirusTotal", "api_key")
        pass

    def fetch_tor_exit_nodes(self):
        r = requests.get(self.tor_exits)

        with open(self.tor_nodes, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return

    def fetch_ip_addresses_from_file(self):
        with open(self.tor_nodes, 'r') as f:
            tors = f.read()
            ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', tors)

            with open(self.tor_ip, 'wb') as exit_ips:
                for ip in ips:
                    if ip:
                        exit_ips.write(ip + "\n")
            return

    def check_ip_is_tor(self, ip):

        if not ip:
            return False

        with open(self.tor_ip) as f:
            for line in f:
                if ip == line:
                    print("%s is tor!" % ip)
                    return True

        return False

    def check_ip_virus_total(self, ip):
        # every 15s scan for ip
        #time.sleep(15)

        try:
            url = "https://www.virustotal.com/vtapi/v2/ip-address/report"
            parameters = {'ip': ip, 'apikey': self.v_total_key}

            r = requests.get(url, params=parameters)
            response = r.json()

            if len(response['detected_urls']) > 3:
                return True

            return False

        except Exception as e:
            print(e)
