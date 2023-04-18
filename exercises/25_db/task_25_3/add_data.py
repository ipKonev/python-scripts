import sqlite3,glob,os,yaml,re

def parse_output(filename):
    regex=re.compile("(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)")
    sw=re.search("(\w+)_dhcp_snooping.txt", filename).group(1)
    with open(filename) as f:
        result = [match.groups() + (sw,) for match in regex.finditer(f.read())]
    return result

def add_rows(connection,query,data):
    #connection=sqlite3.connect(db)
    for row in data:
        try:
            with connection as conn:
                conn.execute(query,row)
        except sqlite3.IntegrityError as e:
            print(f'Error {e} has been occured while adding new data')


def populate_sw(db, sw_data_file):
    print('Populate switches table')
    connection=sqlite3.connect(db)
    query='INSERT into switches values (?, ?)'
    with open(sw_data_file) as f:
        sw=yaml.safe_load(f)
        sw_data=list(sw['switches'].items())
        add_rows(connection,query,sw_data)
    connection.close()

def populate_dhcp(db,data_files):
    #result=[]
    connection=sqlite3.connect(db)
    upd='REPLACE into dhcp values (?, ?, ?, ?, ?, ?)'
    #print('Replacing data in dhcp table')
    connection.execute('UPDATE dhcp set active = 0')
    #query='INSERT into dhcp values (?, ?, ?, ?, ?)'
    for fname in data_files:
        result=parse_output(fname)
        upd_res=(row + (1,) for row in result)
        add_rows(connection,upd,upd_res)
        #result.extend(parse_output(fname))
    connection.close()

if __name__=='__main__':
    db='dhcp_snooping.db'
    files=glob.glob('new_data/sw*_dhcp_snooping.txt')
    #files=glob.glob('sw*_dhcp_snooping.txt')
    exist=os.path.exists(db)
    if exist:
        populate_sw(db,'switches.yml')
        populate_dhcp(db,files)
    else:
        print('Database doesnt exists, please create it before adding new data')
