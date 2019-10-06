import argparse
import logging
import time

import service
from module.users import Users

def addArg():
    parser = argparse.ArgumentParser(description='Block users on twitter')
    parser.add_argument('--authorization', nargs='*')
    parser.add_argument('--url')
    parser.add_argument('--following', action='store_true')
    parser.add_argument('--proxy')
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
        currentUser = allUsers.pop()
        
        if 'blocked' in currentUser:
            continue

        spier.toBlock(currentUser)

        time.sleep(3)

