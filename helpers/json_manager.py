import json
import logging
import os

from helpers.logger_config import logger as log

log = logging.getLogger(__name__)

def json_load(file_path):
    if not os.path.isfile(file_path):
        log.warning(f"{os.path.basename(file_path)} does not exist")
        return 
    else:
        with open(file_path) as file:
            log.info(f"{os.path.basename(file_path)} has loaded")
            return json.load(file)
        
def json_dump(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        log.info(f"{os.path.basename(file_path)} has dumped")
    