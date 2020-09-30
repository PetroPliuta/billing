#! /usr/bin/env python

import radiusd
import requests
import requests_unixsocket


def instantiate(p):
    print "*** instantiate ***"
    print p
    return radiusd.RLM_MODULE_OK


def authenticate(p):
    print '*** authenticate ***'
    print p
    return radiusd.RLM_MODULE_OK


def authorize(p):
    print "*** authorize ***"
    print "NAS request:", p
    with requests_unixsocket.monkeypatch():
        response = requests.post(
            'http+unix://%2Fvar%2Fwww%2Fbilling%2Fbilling.sock/radius_authorize/', json=p, timeout=3)
        print
        print "response code:", response.status_code
        if not response.status_code == 200:
            return radiusd.RLM_MODULE_REJECT
        parsed_response = response.json()
    print "parsed response:", parsed_response
    reply = tuple((str(key), str(value))
                  for key, value in parsed_response["reply"].items())
    print "reply: ", reply
    config = tuple((str(key), str(value))
                   for key, value in parsed_response["config"].items())
    print "config: ", config
    return (radiusd.RLM_MODULE_OK, reply, config)


def pre_proxy(p):
    print "*** pre_proxy ***"
    print p
    return radiusd.RLM_MODULE_OK


def post_proxy(p):
    print "*** post_proxy ***"
    print p
    return radiusd.RLM_MODULE_OK


def post_auth(p):
    print "*** post_auth ***"
    print p
    return radiusd.RLM_MODULE_OK


def recv_coa(p):
    print "*** recv_coa ***"
    print p
    return radiusd.RLM_MODULE_OK


def send_coa(p):
    print "*** send_coa ***"
    print p
    return radiusd.RLM_MODULE_OK


def detach():
    print "*** goodbye from example.py ***"
    return radiusd.RLM_MODULE_OK
