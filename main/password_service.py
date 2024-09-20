from cryptography.fernet import Fernet
from os.path import join, dirname, abspath


_root_folder = dirname(abspath(__file__))
_key = join(_root_folder, 'key.key')
_script = join(_root_folder, 'scripts/encrypted_password_generator.py.enc')

# Load the encryption key
with open(_key, 'rb') as key_file:
    key = key_file.read()

cipher = Fernet(key)

# Load and decrypt the encrypted script
with open(_script, 'rb') as f:
    encrypted_code = f.read()
decrypted_code = cipher.decrypt(encrypted_code).decode('utf-8')

# Execute the decrypted code
word_1 = "Word"
number_1 = "987654321"
exec(decrypted_code)

pg = PasswordGenerator(word_1, number_1)
pg.password()
