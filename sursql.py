#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from MySQLdb import escape_string

def insertInDatabase(table, **args):
    """
    returns valid SQL Code for insertion 
    """
    fields = ','.join(args.keys())
    values = ','.join(['"%s"' % escape_string(i) for i in args.values()])
    return "INSERT INTO %s (%s) VALUES (%s)" % (table, fields, values)

def updateDatabase(table, id, **args):
    """
    returns valid SQL Code for update 
    """
    fieldsAndValues = ','.join(["%s = '%s'" % (i, j) for i,j in args.items()])
    return "UPDATE %s set %s WHERE id = %s" % (table, fieldsAndValues, id)

def selectInDatabase(table, **args):
    """
    returns valid SQL Code for selecting 
    """
    fieldsAndValues = ' AND '.join(["%s = '%s'" % (i, j) for i,j in args.items()])
    return "SELECT * FROM %s WHERE %s" % (table, fieldsAndValues)


if __name__ == '__main__':
    assert insertInDatabase("req_header", id='20', header_t="test") == 'INSERT INTO req_header (header_t,id) VALUES ("test","20")'
    assert updateDatabase("req_header", id='20', header_t="test1", testarg="4") == "UPDATE req_header set header_t = 'test1',testarg = '4' WHERE id = 20"
    assert selectInDatabase("req_header", testarg='4', header_t="test1") == "SELECT * FROM req_header WHERE header_t = 'test1' AND testarg = '4'"


