#! /usr/bin/env python

import radiusd
import requests
import requests_unixsocket


def preacct(p):
    print "*** preacct ***"
    print p
    return radiusd.RLM_MODULE_OK


def accounting(p):
    print "*** accounting ***"
#    radiusd.radlog(radiusd.L_INFO, '*** radlog call in accounting (0) ***')
#    print
    print "NAS request", p
    # NAS
    with requests_unixsocket.monkeypatch():
        response = requests.post(
            'http+unix://%2Fvar%2Fwww%2Fbilling%2Fbilling.sock/radius_accounting/', json=p, timeout=3)
    print "response code:", response.status_code
    if not response.status_code == 200:
        return radiusd.RLM_MODULE_REJECT
    return radiusd.RLM_MODULE_OK
