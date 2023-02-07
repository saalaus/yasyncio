# yasyncio
Async upload files to YandexDisk usind aiohttp.
It is much faster than synchronous download

## Use
### Get token
1. Create app and get token [here](https://yandex.ru/dev/disk/rest/)
2. Set token to variables
`export YANDEX_TOKEN=<token here>`

### Clone
Git clone project into you PC
`git clone https://github.com/saalaus/yasyncio.git`

### Install dependicies
1. Create virtual env
`python -m venv venv`

2. Activate virtual env
`source venv/bin/activate` or `venv/bin/activate.bat` on windows

3. Install dependicies
`pip install -r requiremenets.txt`

### Run app
Run app:

`python yandexdisk.py <dir>`
