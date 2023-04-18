import os
import sqlite3

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

if __name__=='__main__':
    db='dhcp_snooping.db'
    schema='dhcp_snooping_schema.sql'
    create_db(db,schema)
