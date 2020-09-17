#! /usr/bin/env python
#
# Python module example file
# Miguel A.L. Paraz <mparaz@mparaz.com>
#
# $Id: 5950a076783245c589678ec8e9098f5859d5d7fa $

import radiusd
import requests


def instantiate(p):
    print "*** instantiate ***"
    print p
    # return 0 for success or -1 for failure


def authenticate(p):
    print 'authenticate:', p
    return radiusd.RLM_MODULE_OK


def authorize(p):
    print "*** authorize ***"
    print
    radiusd.radlog(radiusd.L_INFO, '*** radlog call in authorize ***')
    print
    print p
    print
    print "radiusd.config:", radiusd.config
    print

    # NAS
    nas_username = ""
    from_nas = dict((x, y) for x, y in p)
    if from_nas['User-Name']:
        nas_username = from_nas['User-Name']
    print "nas_username:", nas_username
    # API
    try:
        r = requests.get(
            "http://127.0.0.1/api/v1/customers/?login="+nas_username)
    except:
        return radiusd.RLM_MODULE_REJECT
    if not r.status_code == 200:
        return radiusd.RLM_MODULE_REJECT
    api_response = r.json()
    print "api_response:", api_response
    if len(api_response) == 0:
        return radiusd.RLM_MODULE_REJECT
    active = api_response[0][u'active']
    balance = api_response[0][u'balance']
    print "active:", active
    print "balance:", balance
    if not active or balance < 0:
        return radiusd.RLM_MODULE_REJECT
    radius_reply = {
        'Acct-Interim-Interval': '60',
    }
    radius_config = {
        'Cleartext-Password': str(api_response[0][u'password'])
    }
    ip = str(api_response[0][u'ip_address'])
    if ip:
        print 'ip address:', ip
        radius_reply['Framed-IP-Address'] = ip
    print 'radius_reply:', tuple(radius_reply.items())
    print 'radius_config:', tuple(radius_config.items())
    return (radiusd.RLM_MODULE_OK, tuple(radius_reply.items()), tuple(radius_config.items()))


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
