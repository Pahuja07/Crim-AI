import logging
import os
import sys
from datetime import datetime

LOG_DIR="logs"
os.makedirs(LOG_DIR,exist_ok=True)
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
LOG_FILE_PATH=os.path.join(LOG_DIR, LOG_FILE)

LOG_FORMAT = "[%(asctime)s] %(levelname)s-%(name)s-%(module)s:%(lineno)d-%(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler(sys.stdout)

    ]
)
logger=logging.getLogger("criminalNetworkLogger")
