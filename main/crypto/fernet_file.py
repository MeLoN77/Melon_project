from cryptography.fernet import Fernet
from os.path import join, dirname, abspath


_root_folder = dirname(dirname(abspath(__file__)))
_key_file = join(_root_folder, 'key.key')
with open(_key_file, "rb") as key:
    _key = key.read()
cipher = Fernet(_key)

_root_folder = dirname(dirname(abspath(__file__)))
path = join(_root_folder, "scripts/password_generator.py")

# Read the Python script to encrypt
with open(path, 'rb') as f:
    code = f.read()

# Encrypt the script
encrypted_code = cipher.encrypt(code)

# Save the encrypted script
with open(f'{_root_folder}/scripts/encrypted_password_generator.py.enc', 'wb') as f:
    f.write(encrypted_code)

