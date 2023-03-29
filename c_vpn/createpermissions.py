from pprint import pprint
from createacl import create_ace, create_acl
from createauthz import create_auth
from readxls import read_xlsx
import colorama
from colorama import Fore, Style

pName,entries=read_xlsx()
#pprint(entries)
#pprint(pName,entries)
ace=create_ace(entries)
colorama.init(autoreset=True)
if create_acl(ace,pName) == 201:
    print('dACL has been created '+Fore.GREEN + 'success')
    if create_auth(pName) == 201:
        print('Authz profile has been created '+Fore.GREEN + 'success')
else:
    print(Fore.RED + 'Something went wrong')
