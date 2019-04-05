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

def get_all_reservations(partition):
    r = pyslurm.reservation()
    res = r.get()
    keys  = r.find("partition", partition)

    reservations = []

    for key in keys:
        tmp = r.find_id(key)
        tmp["name"] = key
        tmp["start_time"] = parse_time(tmp["start_time"])
        tmp["end_time"] = parse_time(tmp["end_time"])
        reservations.append(tmp)

    return reservations

def get_reservation(partition, res_id):
    r = pyslurm.reservation()
    res = r.get()
    keys  = r.find("partition", partition)

    found = False;

    for key in keys:
        if key == res_id:
            res[res_id]['name'] = key
            res[res_id]["start_time"] = parse_time(res[res_id]["start_time"])
            res[res_id]["end_time"] = parse_time(res[res_id]["end_time"])
            found = True;
            break

    if found:
        return res[res_id]
    else:
        return create_dict()

def create_reservation(res_dict):
    r = pyslurm.reservation()
    print (res_dict)
    res_id = r.create(res_dict)
    return res_id

def get_partition(username):
    db = TinyDB('db.json')
    User = Query()
    res = db.search(User.username == username)

    if len(res) > 0:
        partitions = res[0]['partitions']
    else:
        partitions = []

    return partitions

def update_reservation(res_dict):
    r = pyslurm.reservation()
    return r.update(res_dict)

def delete_reservation(res_id, reason):
    r = pyslurm.reservation()
    return r.delete(res_id)
