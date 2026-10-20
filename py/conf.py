
import yaml
import logging
import sys
import os

from pathlib import Path
from datetime import datetime

import utl
import ver

def get(path,info=False):
    if info:
        logging.basicConfig(
           format='%(levelname)s:%(module)s:%(funcName)s():: %(message)s',
           level=logging.INFO
        )
    else:
        logging.basicConfig(
           format='%(levelname)s:%(module)s:%(funcName)s():: %(message)s',
        )
    logging.info("getting config file from "+path )
    with open(path, 'r') as file:
       config = yaml.safe_load(file)


    config['ban'] = ver.ban()
    config['chat'] = config['url'] + "/" +config['chatPath']    
    config['tags'] = config['url'] + "/" +config['tagsPath']    

    return config



