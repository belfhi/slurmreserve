#!/usr/bin/env python3

import time
import datetime
import sys
import pyslurm 
from tinydb import TinyDB, Query

def parse_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S')

#def parse_reservation():
#    pass

def create_dict():
    res_dict = pyslurm.create_reservation_dict()
    return res_dict

def get_reservation(partition):
	r = pyslurm.reservation()
	res = r.get()
	keys  = r.find("partition", partition)

	reservations = []

	for key in keys:
		tmp = r.find_id(key)
		tmp["start_time"] = parse_time(tmp["start_time"])
		tmp["end_time"] = parse_time(tmp["end_time"])
		reservations.append(tmp)

	return reservations

def create_reservation(res_dict)
    r = pyslurm.reservation()
    res_id = r.create(res_dict)
    return res_id

def get_partition(username):
    db = TinyDB('db.json')
    User = Query()
    res = db.search(User.username == username)[0]
    partitions = res['partition']

    return partitions

def update_reservation(res_dict):
	r = pyslurm.reservation()
    r.update(res_dict)
    return 

def delete_reservation(res_id, reason):
	r = pyslurm.reservation()
    r.delete(res_id, reason)
    return
