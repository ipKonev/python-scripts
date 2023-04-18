import sqlite3,os,re,yaml
from datetime import timedelta,datetime
from tabulate import tabulate

def create_db(db, schema):
    exist=os.path.exists(db)
    if exist:
        print('Database already created')
        return None
    print('Database creation in process')
    with open(schema) as f:
        f_s=f.read()
        connection=sqlite3.connect(db)
        connection.executescript(f_s)
        connection.close()

def remove_old(connection):
    now=datetime.today().replace(microsecond=0)
    week_ago=str(now-timedelta(days=7))
    query='DELETE from dhcp where last_active < ?'
    connection.execute(query, (week_ago,))
    connection.commit()

def add_data(db,data_files):
    connection=sqlite3.connect(db)
    remove_old(connection)
    upd='REPLACE into dhcp values (?, ?, ?, ?, ?, ?, datetime("now"))'
    connection.execute('UPDATE dhcp set active = 0')
    connection.commit()
    for fname in data_files:
        result=parse_output(fname)
        upd_res=(row + (1,) for row in result)
        add_rows(connection,upd,upd_res)
    connection.close()

def parse_output(filename):
    regex=re.compile("(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)")
    sw=re.search("(\w+)_dhcp_snooping.txt", filename).group(1)
    with open(filename) as f:
        result = [match.groups() + (sw,) for match in regex.finditer(f.read())]
    return result

def add_rows(connection,query,data):
    for row in data:
        try:
            with connection as conn:
                conn.execute(query,row)
        except sqlite3.IntegrityError as e:
            print(f'Error {e} has been occured while adding new data')

def add_data_switches(db, sw_data_file):
    print('Populate switches table')
    connection=sqlite3.connect(db)
    query='INSERT into switches values (?, ?)'
    for fname in sw_data_file:
        with open(sw_data_file) as f:
            sw=yaml.safe_load(f)
        sw_data=list(sw['switches'].items())
        add_rows(connection,query,sw_data)
    connection.close()

def value_checking(db,args):
    if not args:
        select_all(db)
    elif len(args) == 2:
        k,v=args
        get_data(db,k,v)
    else:
        print('You must define only 0 or 2 args')

def get_data(db,key,value):
    list1=['mac','ip','vlan','interface','switch','active']
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

def get_all_data(db):
    connection=sqlite3.connect(db)
    query='SELECT * from dhcp where active = ?'
    for i in (1,0):
        result=connection.execute(query, (i,))
        if i == 1:
            print('Активные записи: ')
            print(tabulate(result))
        elif i == 0:
            print('Нективные записи: ')
            print(tabulate(result))
