#!/usr/bin/env python

import sys
from tinydb import TinyDB, Query

db = TinyDB('slurmreserve/db.json')
username = input('Enter Username: ')
User = Query()
result = db.search(User.username == username)

if len(result) > 0:
    result = result[0]
    print('your current allowed partitions are: {}'.format(result['partitions']))
    while True:
        result = db.search(User.username == username)[0]
        y = input('add another partition? y/n ')
        if y == 'y':
            part_new = input('Enter new partition name(s): ').replace(',', ' ').split()
            if part_new:
                partitions = result['partitions'] + part_new
                db.update({ 'partitions' : list(set(partitions))}, User.username == username)
            else:
                print('no new partitions given')
        else:
            break
        
    
else:
    y = input('User not found, create new? y/n: ')
    if y == 'y':
        db.insert({'username': username, 'partitions': []})
        while True:
            result = db.search(User.username == username)[0]
            part_new = input('Enter partition to be added: ').replace(',', ' ').split()
            if part_new:
                partitions = result['partitions'] + part_new
                db.update({'partition': list(set(partitions))}, User.username == username)
            else:
                break
    elif y == 'n':
        sys.exit(0)
    else:
        print('enter y or n')
        sys.exit(1)
