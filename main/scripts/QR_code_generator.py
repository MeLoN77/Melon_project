import segno
import os


places = {
    "Site": "https://gidmallorca.com/top-10-dostoprimechatelnostej-majorki",
}



def generate_qr_codes(links: dict):
    abs_path = os.path.dirname(os.path.abspath('QR_code_generator.py'))
    _dir_qr_codes = f"{abs_path}/QR_codes/"
    if not os.path.exists(_dir_qr_codes):
        os.mkdir(_dir_qr_codes)

    for name, url in links.items():
        qrcode = segno.make_qr(url)
        qrcode.save(f"{_dir_qr_codes}/{name}.png", scale=5)
