#!/usr/bin/python
import time
import re
import subprocess
import os
import iptc

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':
    logfile = open("/var/log/secure","r")
    loglines = follow(logfile)
    ipNew = 999
    ipOld = 999
    count = 0
    for line in loglines:
        if re.search(r"Failed password", line):
                ipNew = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
                if ipNew == ipOld:
                        count += 1
                else:
                     	count = 0
                        ipOld = ipNew
       if count > 4:
		count = 0
		ipString = str(ipNew)

		rule = iptc.Rule()
		rule.protocol = "tcp"
		match = iptc.Match(rule, "tcp")
		match.dport = "22"
		ule.add_match(match)
		match = iptc.Match(rule, "ip")
		match.src = ipString
		rule.add_match(match)
		rule.target = iptc.Target(rule, "DROP")
		chain = iptc.Chain(iptc.Table.(iptc.Table.FILTER), "INPUT")
		chain.insert_rule(rule)

