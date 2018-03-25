from argparse import ArgumentParser
from subprocess import Popen, PIPE
from urllib.request import urlopen
import json
import re

def trace_route(target):
    p = Popen(["tracert", target], stdout=PIPE, shell=True)
    ip_search = re.compile('\d+.*[ \[](\d+\.\d+\.\d+\.\d+)')
    while True:
        line = p.stdout.readline().decode()
        if line == '': break
        hop_ip = ip_search.search(line)
        AS_data = "***"
        if hop_ip:
            AS_data = get_AS_data(hop_ip.group(1))
        print("{0}{2}{1:<40}".format(line[:-2], AS_data, " " * (80 - len(line))))

def get_AS_data(ip):
    data = dict(json.loads(urlopen(f'http://ipinfo.io/{ip}/json').read()))
    keys = ["country", "region", "city", "org"]
    if "bogon" in data and data["bogon"]:
        return "private network"
    return ' '.join([data[key] for key in keys if key in data])


if __name__ == '__main__':
    parser = ArgumentParser("Basic trace autonomous systems tool")
    parser.add_argument('target', type=str, help='Target hostname')
    trace_route(parser.parse_args().target)