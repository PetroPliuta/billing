#! /usr/bin/env python

import radiusd
import requests
from datetime import datetime


def preacct(p):
    print "*** preacct ***"
    print p
    return radiusd.RLM_MODULE_OK


def user_online(login, online=True):
    print "online:" if online else "offline:", login
    url = 'http://127.0.0.1/api/v1/customers/'
    try:
        r = requests.get(url+"?login="+login)
        response = r.json()
        result = response[0]
        print "result:", result

        customer_id = str(result[u'id'])
        data = result
        data['online'] = online

    # datetime object containing current date and time
        now = datetime.now()
        print "now =", now
        data['last_online'] = now

        r = requests.put(url+customer_id+'/', data)
        print "change online status response:", r.text
    except:
        print "change online status error"


def accounting(p):
    print "*** accounting ***"
    radiusd.radlog(radiusd.L_INFO, '*** radlog call in accounting (0) ***')
    print
    print p
    # NAS
    from_nas = dict((x, y) for x, y in p)
    acct_type = from_nas['Acct-Status-Type'] if from_nas['Acct-Status-Type'] else ''
    nas_username = from_nas['User-Name'] if from_nas['User-Name'] else ''

    if acct_type == 'Start' or acct_type == 'Interim-Update':
        user_online(nas_username)
    if acct_type == 'Stop':
        user_online(nas_username, False)

    return radiusd.RLM_MODULE_OK
