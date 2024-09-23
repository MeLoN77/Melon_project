import os
import shutil
import segno
from main.logs.melon_logs import log

ABS_PATH = os.path.dirname(os.path.abspath('helpers.py'))
_DIR_QR_CODES = f"{ABS_PATH}/QR_codes/"


def qr_code(link: str, chat_id: str):
    """
    Generates QR Code from LINK to the resource
    :param link: str
    :param chat_id: str
    :return:
    """
    if not os.path.exists(_DIR_QR_CODES):
        os.mkdir(_DIR_QR_CODES)
    if "http" not in link:
        return False

    qrcode = segno.make_qr(link)
    path_to_save = f"{_DIR_QR_CODES}/qrcode_{chat_id}.png"
    qrcode.save(path_to_save, scale=5)
    log.info('Generating new QR Code.')
    return path_to_save


def remove_qr_codes():
    shutil.rmtree(_DIR_QR_CODES)
    log.info(f'Removing QR Code directory: {_DIR_QR_CODES}')
