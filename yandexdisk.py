import asyncio
import logging
import os
from pathlib import Path
from sys import argv
import time
from typing import Literal

from aiohttp import ClientSession

from settings import HEADERS, API_URL, logger, TOKEN


start_time = time.time()
file_tasks = []


async def upload_file(
        session: ClientSession,
        file: str | Path,
        fold: str = "",
        overwrite: Literal["true", "false"] = "true"):
    """upload files on yandex disk
    session = ClientSession
    file = path file to upload
    fold = folder in yandex disk to upload
    overwrite = overwrite in yandex disk
    """
    url = API_URL+"/upload"
    params = {
        "path": fold,
        "overwrite": overwrite,
    }
    async with session.get(
            url,
            params=params,
            headers=HEADERS) as response:
        r = (await response.json())["href"]
        with open(file, 'rb') as f:
            async with session.put(r, data={"file": f}) as response2:
                logger.info(f'File {fold} was created')
                return await response2.read()


async def mkdir(session: ClientSession, path: Path | str):
    """make directory in yandex disk
    session = ClientSession
    path = path to folder in yandex disk
    """
    params = {
        "path": path
    }
    async with session.put(
            API_URL,
            params=params,
            headers=HEADERS) as response:
        r = await response.read()
        logger.info(f'Fold {path} was created')
        return r


async def scan_dir(session: ClientSession, path: Path | str = ".", yandex_path: str = ""):
    """Scan directory, finds folders and files, and run upload him
    session = ClientSession
    path = path to scan
    yandex_path = path to yandex disk
    """
    scan_path = Path(path)
    folds = [x for x in scan_path.iterdir() if x.is_dir()]
    files = [x for x in scan_path.iterdir() if x.is_file()]
    for fold in folds:
        path = str(Path(yandex_path)/fold.name)
        await mkdir(session, path)
        await scan_dir(session, fold, path)
    for file in files:
        path = str(Path(yandex_path)/file.name)
        file_tasks.append(asyncio.create_task(
            upload_file(session, file,
                        path)
        )
        )


async def main():
    session = ClientSession()

    await scan_dir(session, argv[-1])
    await asyncio.gather(*file_tasks)

    await session.close()

    logger.info(time.time() - start_time)


asyncio.run(main())
