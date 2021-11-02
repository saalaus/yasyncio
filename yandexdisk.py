import asyncio
from aiohttp import ClientSession
from os import path, listdir, rename
from sys import argv
import requests
import time
import logging

# logger = logging.getLogger("yasyncio")
# logging.basicConfig(filename='logs.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


TOKEN = 'AQAAAABEwImmAAcQ84dL9_0pREQYpntlSCuWmtQ'


start_time = time.time()
HEADERS = {'Authorization': 'OAuth {}'.format(TOKEN)}

# функция для загрузки файлов на яндекс диск
async def upload_file(file, fold=""):
    async with session.get('https://cloud-api.yandex.net/v1/disk/resources/upload', params=dict(path=fold, overwrite='True'), headers=HEADERS) as response:
        r = await response.json()
        # print(r)
        r = r['href']
        with open(file, 'rb') as f:
            async with session.put(r, data=dict(file=f)) as response2:
                # logger.info(f'Файл {file} создан')
                return await response2.read()


# функция для создания папок на яндекс диске
async def mkdir(path):
    async with session.put('https://cloud-api.yandex.net/v1/disk/resources', params=(dict(path=path)), headers=HEADERS) as response:
        r = await response.read()
        # logger.info(f'Папка {path} создана')
        return r


# функция для поиска файлов и папок в заданной директории
async def scan_dir(file, folder='', yandex_dir=''):
    dir = list(path.split(file))
    dir[0] = path.join(dir[0], folder)
    file = path.join(dir[0], dir[1])
    if path.isfile(file):
        tasks.append(loop.create_task(upload_file(file.replace(
            '\\', '/'), path.normpath(path.join(yandex_dir, dir[1])).replace('\\', '/'))))
    else:
        yandex_dir = path.join(yandex_dir, dir[1])
        await mkdir(path.normpath(yandex_dir).replace('\\', '/'))
        for i in listdir(file):
            await scan_dir(path.join(dir[0], i),
                               dir[1],
                               yandex_dir
                               )


async def create_session():
    return ClientSession()


async def close_session(session):
    return await session.close()


try:
    loop = asyncio.new_event_loop()
    tasks = []

    session = loop.run_until_complete(create_session())

    print("сканирование директории")
    loop.run_until_complete(scan_dir('C:\\Users\\User\\Desktop\\python_projects'))
    print("завершение сканирования")
    loop.run_until_complete(asyncio.gather(*tasks))
    print("завершение выложения")
    asyncio.run(close_session(session))
    loop.close()
    # loop.run_until_complete(main())
    print(time.time() - start_time)
except Exception as e:
    print(e)
    # logger.critical(e)
