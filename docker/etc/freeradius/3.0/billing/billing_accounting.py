#! /usr/bin/env python

import radiusd
import requests
from datetime import datetime

customers_url = 'http://127.0.0.1/api/v1/customers/'
routers_url = 'http://127.0.0.1/api/v1/routers/'


def preacct(p):
    print "*** preacct ***"
    print p
    return radiusd.RLM_MODULE_OK


def get_customer(login):
    global customers_url
    r = requests.get(customers_url+"?login="+login)
    return r.json()[0]


def set_online(login, online=True):
    global customers_url
    print("online" if online else "offline")+" login:", login
    try:
        data = get_customer(login)

        data['online'] = online

        r = requests.put(customers_url+str(data['id'])+'/', data)
    #    print "set_online response:" , r.text
    except Exception as inst:
        print "set_online/offline status error:", inst
    else:
        print "set_online/offline status - ok"


def set_last_datetime(login):
    global customers_url
    try:
        data = get_customer(login)

        now = datetime.now()
        data['last_online_datetime'] = now

        r = requests.put(customers_url+str(data['id'])+'/', data)
#        print "set_last_datetime response:" , r.text
    except Exception as inst:
        print "set_last_datetime error:", inst
    else:
        print "set_last_datetime - ok"


def set_last_ip(from_nas):
    global customers_url
    try:
        login = from_nas['User-Name']
        data = get_customer(login)

        data['last_online_ip'] = from_nas['Framed-IP-Address']

        r = requests.put(customers_url+str(data['id'])+'/', data)
#        print "set_last_datetime response:" , r.text
    except Exception as inst:
        print "set_last_ip error:", inst
    else:
        print "set_last_ip - ok"


def get_router(ip):
    global routers_url
    r = requests.get(routers_url+"?ip_address="+str(ip))
    return r.json()[0]


def set_last_router(from_nas):
    global customers_url
    try:
        router = get_router(from_nas['NAS-IP-Address'])

        login = from_nas['User-Name']
        data = get_customer(login)

        data['last_online_router'] = router['id']

        r = requests.put(customers_url+str(data['id'])+'/', data)
#        print "set_last_datetime response:" , r.text
    except Exception as inst:
        print "set_last_router error:", inst
    else:
        print "set_last_router - ok"


def accounting(p):
    print "*** accounting ***"
    # NAS
    from_nas = dict((x, y) for x, y in p)
    acct_type = from_nas['Acct-Status-Type'] if from_nas['Acct-Status-Type'] else ''
    nas_username = from_nas['User-Name'] if from_nas['User-Name'] else ''

    if acct_type.lower() == 'start' or acct_type.lower() == 'interim-update':
        set_online(nas_username)
    if acct_type.lower() == 'stop':
        set_online(nas_username, False)

    set_last_datetime(nas_username)
    set_last_ip(from_nas)
    set_last_router(from_nas)

    return radiusd.RLM_MODULE_OK
