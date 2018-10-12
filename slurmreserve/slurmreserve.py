#!/usr/bin/env python3

import time
import datetime
import sys
import pyslurm 

def parse_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S')

def parse_reservation():
    pass

def create_dict():
    return res_dict

def get_reservation(partition):
	r = pyslurm.reservation()
	res = r.get()
	keys  = res.find("partition", partition)

	reservations = []

	for key in keys:
		tmp = res.find_id(key)
		tmp["start_time"] = parse_time(tmp["start_time"])
		tmp["end_time"] = parse_time(tmp["end_time"])
		reservations.append(tmp)

	return reservations

def create_reservation(partition, *args):
    return res_id

def get_partition(username):
	#Read users patitions from db
	partitions = ["cms"]

	return partitions

def update_reservation(res_dict):
    return 

def delete_reservation(res_id, reason):
    return
