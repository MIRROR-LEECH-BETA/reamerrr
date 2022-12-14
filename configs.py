# (c) @AbirHasan2005

import os
import logging

logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler()],
    level=logging.INFO
)


class Config(object):
    API_ID = int(os.environ.get("API_ID", "14417186"))
    API_HASH = os.environ.get("API_HASH", "21731d919d79f78de24bdf1f6ccd6921")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "5725315353:AAG_3r6eaK9zK4FYThl4ndMs1Ue9LSm6S2c")
    DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", "./downloads")
    LOGGER = logging
    OWNER_ID = int(os.environ.get("OWNER_ID", "5558249587"))
    PRO_USERS = list(set(int(x) for x in os.environ.get("PRO_USERS", "0").split()))
    PRO_USERS.append(OWNER_ID)
    FORCE_SUB = os.environ.get("FORCE_SUB", "beta_botz")
    MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb+srv://RENAME:RENAME@cluster0.0qshmty.mongodb.net/?retryWrites=true&w=majority")
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001545756568"))
    BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", "True"))
