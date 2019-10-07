import argparse
import logging
import time
import asyncio

import service
from module.users import Users
from module.error import SpierEnd

allUsers = Users([])

def addArg():
    parser = argparse.ArgumentParser(description='Block users on twitter')
    parser.add_argument('--authorization')
    parser.add_argument('--url')
    parser.add_argument('--following', action='store_true')
    parser.add_argument('--proxy')
    args = parser.parse_args()
    return args

async def asyncGetUser(classSpier):
    global allUsers
    while True:
        await asyncio.sleep(30)
        try:
            users = classSpier.getUsers()
        except SpierEnd:
            print('用户全部获取')
            break
        allUsers += users

async def asyncBlockUser(classSpier):
    while len(allUsers):
        currentUser = allUsers.pop(0)
        
        if currentUser['blocked']:
            continue

        status = classSpier.toBlock(currentUser)
        print(status)

        await asyncio.sleep(3)

async def main():
    global allUsers

    args = addArg()

    spier = service.getSpier(args)

    allUsers += spier.getUsers()

    await asyncio.gather(
        asyncGetUser(spier),
        asyncBlockUser(spier)
    )

if __name__ == "__main__":
    asyncio.run(main())