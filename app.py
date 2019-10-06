import argparse
import logging
import time

import service
from module.users import Users

def addArg():
    parser = argparse.ArgumentParser(description='Block users on twitter')
    parser.add_argument('--authorization')
    parser.add_argument('--url')
    parser.add_argument('--following', action='store_true')
    parser.add_argument('--proxy')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = addArg()

    spier = service.getSpier(args)

    (users, pageTotal) = spier.getUsers()

    allUsers = Users(users)

    while True:
        time.sleep(1)
        (users, _) = spier.getUsers()
        allUsers += users
        if len(allUsers) == int(pageTotal) or spier.page == 5:
            break

    while len(allUsers):
        currentUser = allUsers.pop(0)
        
        if 'blocked' in currentUser:
            print('pass', currentUser['uname'])
            continue

        spier.toBlock(currentUser)
        print('block', currentUser['uname'])

        time.sleep(3)

