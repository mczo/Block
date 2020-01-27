import argparse
import logging
import time
import asyncio

import service
from module.users import Users
from module.error import SpierEnd

allUsers = Users([])

getting = True

def addArg():
    parser = argparse.ArgumentParser(description='Block users on twitter')
    groupAuth = parser.add_argument_group('auth')
    groupAuth.add_argument('--authorization')
    groupAuth.add_argument('--cookie')

    parser.add_argument('--url')
    parser.add_argument('--proxy')
    args = parser.parse_args()
    return args

async def asyncGetUser(classSpier):
    global allUsers, getting
    while True:
        await asyncio.sleep(20)
        try:
            users = classSpier.getUsers()
        except SpierEnd:
            print('用户全部获取')
            getting = False
            break
        allUsers += users

async def asyncBlockUser(classSpier):
    global getting

    while len(allUsers) or getting:
        if not len(allUsers): continue
        currentUser = allUsers.pop(0)
        if currentUser['blocked']: continue

        res = classSpier.toBlock(currentUser)

        if res:
            print('已屏蔽：%s' % res['name'])
        else:
            print('未屏蔽：%s' % res['name'])

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