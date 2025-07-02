#!/usr/bin/env python3

import argparse
import getpass
import requests
import json
import sys

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def parse_args():
    '''Parse command line arguments'''

    parser = argparse.ArgumentParser()

    parser.add_argument('--hostname',
                        required=True,
                        help="Specify the NMC hostname")

    parser.add_argument('--username',
                        required=True,
                        help="Specify the username")

    parser.add_argument('--password',
                        required=False,
                        help="Specify the password")

    args = parser.parse_args()

    if not args.password:

        args.password = getpass.getpass(f"Please enter the password for {args.username}: ")
 
    return args

def get_token(args):
    '''Retrieve access token'''

    resource = f'https://{args.hostname}/api/v1.1/auth/login/'

    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}

    creds = {'username': args.username,
             'password': args.password}

    request = requests.post(url=resource,
                            headers=headers,
                            data=json.dumps(creds),
                            verify=False)
    if not request.ok:
    
        print(json.dumps(request.json(), indent=4))
        sys.exit()

    return request.json()

def get_data(args, token):
    '''Retrieve access token'''

    resource = f'https://{args.hostname}/api/v1.1/volumes'

    headers = {'Content-Type': 'application/json',
               'Authorization': f'Token {token}'}

    request = requests.get(url=resource,
                           headers=headers,
                           verify=False)
    if not request.ok:
    
        print(json.dumps(request.json(), indent=4))
        sys.exit()

    return json.dumps(request.json(), indent=4)

def main():
    '''Main'''

    args = parse_args()

    token = get_token(args)

    print(token['token'])

    data = get_data(args, token['token'])

    print(data)

if __name__ == '__main__':

    main()