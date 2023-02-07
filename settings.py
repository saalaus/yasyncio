import logging
import os


logger = logging.getLogger("yasyncio")
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("YANDEX_TOKEN")

API_URL = "https://cloud-api.yandex.net/v1/disk/resources"
HEADERS = {'Authorization': f'OAuth {TOKEN}'}
