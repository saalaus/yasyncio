import asyncio
import logging
import time
from pathlib import Path
from sys import argv

from aiohttp import ClientSession


logger = logging.getLogger("yasyncio")

logging.basicConfig(level=logging.DEBUG)


TOKEN = 'TOKEN'


start_time = time.time()
API_URL = "https://cloud-api.yandex.net/v1/disk/resources"
HEADERS = {'Authorization': 'OAuth {}'.format(TOKEN)}
file_tasks = []


# upload files on yandex disk
async def upload_file(session, file, fold="", overwrite="true"):
    async with session.get(API_URL+'/upload', params=dict(path=fold, overwrite=overwrite), headers=HEADERS)\
        as response:
        r = (await response.json())["href"]
        with open(file, 'rb') as f:
            async with session.put(r, data=dict(file=f)) as response2:
                logger.info(f'File {fold} was created')
                return await response2.read()


# mkdir folder on yandex disk
async def mkdir(session, path):
    async with session.put(API_URL, params=(dict(path=str(path))), headers=HEADERS)\
        as response:
        r = await response.read()
        logger.info(f'Fold {path} was created')
        return r


async def scan_dir(session: ClientSession, path=".", yandex_path=""):
    p = Path(path)
    folds = [x for x in p.iterdir() if x.is_dir()]
    files = [x for x in p.iterdir() if x.is_file()]
    for fold in folds:
        path = str(Path(yandex_path)/fold.name).replace("\\", "/")
        await mkdir(session, path)
        await scan_dir(session, fold, path)
    for file in files:
        path = str(Path(yandex_path)/file.name).replace("\\", "/")
        file_tasks.append(asyncio.create_task(
            upload_file(session, file, path)))


async def main():
    session = ClientSession()

    await scan_dir(session, argv[-1])
    await asyncio.gather(*file_tasks)

    await session.close()

    logger.info(time.time() - start_time)


asyncio.get_event_loop().run_until_complete(main())
