#!/usr/bin/env python

import sys
from tinydb import TinyDB, Query

class Database:
    def __init__(self, dbfile=None):
        if dbfile == None:
            dbfile = 'db.json'
        self.db = TinyDB(dbfile)
        self.User = Query()

    def get_userentry(self, username):
        result = self.db.search(self.User.username == username)
        return result

    def add_user(self, username):
        if not self.check_user(username):
            self.db.insert({'username': username, 'partitions':[]})
        return

    def check_user(self, username):
        res = self.get_userentry(username)
        if len(res) == 0:
            return False
        else:
            return True
       
    def add_partition(self, user, partition):
        partitions = result['partitions'] + part_new
        self.db.update({ 'partitions' : list(set(partitions))}, User.username == username)
        return 

if __name__ == '__main__':
    DB = Database()
    username = input('Enter Username: ')
    User = Query()
    if not DB.check_user(username):
        pass
        
    result = DB.get_userentry(username)


    if len(result) > 0:
        result = result[0]
        print('your current allowed partitions are: {}'.format(result['partitions']))
        while True:
            y = input('add another partition? y/n ')
            if y == 'y':
                part_new = input('Enter new partition name(s): ').replace(',', ' ').split()
                if part_new:
                    DB.add_partition(username, part_new)
                else:
                    print('no new partitions given')
            else:
                break
            
        
    else:
        y = input('User not found, create new? y/n: ')
        if y == 'y':
            DB.insert({'username': username, 'partitions': []})
            while True:
                result = DB.search(User.username == username)[0]
                part_new = input('Enter partition to be added: ').replace(',', ' ').split()
                if part_new:
                    partitions = result['partitions'] + part_new
                    DB.update({'partitions': list(set(partitions))}, User.username == username)
                else:
                    break
        elif y == 'n':
            sys.exit(0)
        else:
            print('enter y or n')
            sys.exit(0)

