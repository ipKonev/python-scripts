import sqlite3,glob,os,yaml,re

def parse_output(filename):
    regex=re.compile("(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)")
    sw=re.search("(\w+)_dhcp_snooping.txt", filename).group(1)
    with open(filename) as f:
        result = [match.groups() + (sw,) for match in regex.finditer(f.read())]
    return result

def add_rows(db,query,data):
    connection=sqlite3.connect(db)
    for row in data:
        try:
            with connection:
                connection.execute(query,row)
        except sqlite3.IntegrityError as e:
            print(f'Error {e} has been occured while adding new data')
    connection.close()

def populate_sw(db, sw_data_file):
    exist=os.path.exists(db)
    if not exist:
        print('Database doesnt exists, please create it before adding new data')
        return None
    print('Populate switches table')
    query='INSERT into switches values (?, ?)'
    with open(sw_data_file) as f:
        sw=yaml.safe_load(f)
    sw_data=list(sw['switches'].items())
    add_rows(db,query,sw_data)

def populate_dhcp(db,data_files):
    result=[]
    exist=os.path.exists(db)
    if not exist:
        print('Database doesnt exists, please create it before adding new data')
        return None
    print('Adding new data in dhcp table')
    query='INSERT into dhcp values (?, ?, ?, ?, ?)'
    for fname in data_files:
        result.extend(parse_output(fname))
    add_rows(db,query,result)

if __name__=='__main__':
    db='dhcp_snooping.db'
    files=glob.glob('sw*_dhcp_snooping.txt')
    populate_sw(db,'switches.yml')
    populate_dhcp(db,files)
