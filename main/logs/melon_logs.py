import logging
import logging.handlers
import os
from os.path import join, dirname, abspath
import time

from datetime import datetime
from colorlog import ColoredFormatter


def __setup_logger():
    """Return a logger with a default ColoredFormatter."""
    formatter = ColoredFormatter(
        "%(log_color)s[%(asctime)s] %(levelname)-8s%(reset)s %(log_color)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red'}
    )

    set_log_lvl = logging.DEBUG
    logger = logging.getLogger('example')
    _time = f"{datetime.now().strftime('%d_%m_%Y')}_{time.strftime('%H')}"
    _project_logs = 'project_logs'
    _file_name = f'{_project_logs}/log_{_time}.log'
    _root_folder = dirname(dirname(abspath(__file__)))
    path = join(_root_folder, _file_name)
    _dir_path = join(_root_folder, _project_logs)
    if not os.path.exists(_dir_path):
        os.mkdir(_dir_path)

    logging.basicConfig(filename=path,
                        filemode='a',
                        format='[%(asctime)s,%(msecs)d] [%(levelname)s] %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(set_log_lvl)
    return logger


log = __setup_logger()

