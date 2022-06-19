from getpass import getpass
import ldap3
from ldap3 import Server, Connection, SUBTREE
from ldap3.extend.microsoft.addMembersToGroups import ad_add_members_to_groups as ad_mtg
from ldap3.extend.microsoft.removeMembersFromGroups import ad_remove_members_from_groups as ad_rfg



def ad_membership(filename=None):
'''
This function add/remove users to/from AD group
function gets filename as an argument
function asks all necessary info to successfully connect to AD DC
'''

    username = input('enter username authorized to perform AD manipulation: ')
    password = getpass('enter password: ')
    dc = input('enter the IP address of AD DC: ')
    
    while True:
        action = input('What kind of manipulation you want to do? :[rem(remove)/add(add)]')
        group_id = input('Enter name of the group you want to perform action: ')
        if (action == 'rem' or action == 'add') and group_id:
            break

    ldap_conn=ldap3.Connection(dc,user=username,password=password)
    ldap_conn.bind()
    
#Находим groupDN 
    ldap_conn.search('dc=DOMAIN,dc=DOMAINNAME,dc=COM', f'(cn={group_id})', SUBTREE)
    group_dn=str(ldap_conn.entries).split(' - ')[0].replace('[DN: ','')
    
    with open(filename) as f:
        for line in f:
            ldap_conn.search('dc=DOMAIN,dc=DOMAINNAME,dc=COM', f'(sAMAccountName={user_id})', SUBTREE)
            #Находим userDN по employeeID
    #l.search('dc=DOMAIN,dc=DOMAINNAME,dc=COM', f'(employeeID={user_id})', SUBTREE)
            user_dn=str(ldap_conn.entries).split(' - ')[0].replace('[DN: ','')
            if action == 'rem':
                    try:
                        rm = ad_rfg(l,udn,gdn,fix=True)
                        print(rm)
                    except ldap3.core.exceptions.LDAPInvalidDnError:
                        print(f'User with employeeID {user_id} probably was blocked')
            elif action == 'add':
                add = ad_mtg(ldap_conn,user_dn,group_dn)
                print(add)
    return 'Done'
    

if __name__=='__main__':
    print(ad_membership('sama.txt')