#!/usr/bin/env python

import requests

import sys


def abort(msg):
    print msg
    sys.exit(1)

if len(sys.argv) != 2:
    abort('Usage: get_user_id.py <token>')

r = requests.get(
    'https://api.telegram.org/bot{}/GetUpdates'.format(sys.argv[1])
)
if r.status_code != 200:
    abort('Server returned {} - aborting'.format(r.status_code))
content = r.json()
if not content['ok']:
    abort('Telegram returned an error')
print content['result'][0]['message']['from']['id']
