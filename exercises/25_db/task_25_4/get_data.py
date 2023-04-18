import sqlite3,sys,os
from tabulate import tabulate

active=1
inactive=0

def select_all(db):
    connection=sqlite3.connect(db)
    #result1=connection.execute("SELECT * from dhcp where active = 1")
    #result1=connection.execute("SELECT * from dhcp where active = 0")
    query='SELECT * from dhcp where active = ?'
    for i in (1,0):
        result=connection.execute(query, (i,))
        if i == 1:
            print('Активные записи: ')
            print(tabulate(result))
        elif i == 0:
            print('Нективные записи: ')
            print(tabulate(result))

def get_data(db,key,value):
    if key not in list1:
        print(f'Supported params are {",".join(list1)}')
        return
    connection=sqlite3.connect(db)
    query=f'SELECT * from dhcp where {key} = ? and active = ?'
    for i in (1,0):
        result=connection.execute(query, (value,i))
        if i == 1:
            print('Активные записи: ')
            print(tabulate(result))
        elif i == 0:
            print('Нективные записи: ')
            print(tabulate(result))

#def single_key(db,key):
#    connection=sqlite3.connect(db)
#    query=f'SELECT * from dhcp where {key}'
#    result=connection.execute(query)
#    print(tabulate(result))

def value_checking(db,args):
    if not args:
        select_all(db)
#    elif len(args) == 1:
#        single_key(db,args)
    elif len(args) == 2:
        k,v=args
        get_data(db,k,v)
    else:
        print('You must define only 0 or 2 args')

list1=['mac','ip','vlan','interface','switch','active']
if __name__=='__main__':
    db='dhcp_snooping.db'
    if os.path.exists(db):
        args=sys.argv[1:]
        #print(args)
        value_checking(db,args)
    else:
        print(f'\n{db} doesnt found in current directory, please validate path')
