from importlib.resources import contents
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import argparse

# REFERENCES
# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/
# https://cryptography.io/en/latest/hazmat/primitives/padding/
# https://www.pythontutorial.net/python-basics/python-read-text-file/#:~:text=To%20read%20a%20text%20file%20in%20Python%2C%20you%20follow%20these,the%20file%20close()%20method.
# https://www.easytweaks.com/python-write-to-text-file/
# https://towardsdatascience.com/a-simple-guide-to-command-line-arguments-with-argparse-6824c30ab1c3
# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.modes.GCM

dir_path = Path("Add your path here")

parser = argparse.ArgumentParser(description='5 arguments')
parser.add_argument('-key', help='key file')
parser.add_argument('-IV', help='IV file')
parser.add_argument('-mode', help='mode')
parser.add_argument('-input', help='input')
parser.add_argument('-out', help='output')
parser.add_argument('-gcm_arg', help='gcm_arg')
args = parser.parse_args()

with open(args.key,'r') as f:
    key = f.read()
    print(key)
f.close()
key = bytes.fromhex(key)
print('hex to bytes key')
print(key)
print(len(key))

mode = args.mode
print(mode)

if mode == 'cbc' or mode == 'gcm':
    with open(args.IV,'r') as f:
        iv = f.read()
    f.close()
    iv = bytes.fromhex(iv)
    print(iv)
    print(len(iv))
elif mode == 'ecb': 
     print('NO IV IN ECB MODE')

with open(args.input,'rb') as f:
    inputmsg = f.read()
f.close()
print(inputmsg)

padded_input = ''
padder = padding.PKCS7(128).padder()
padded_input = padder.update(inputmsg)
padded_input += padder.finalize()
print(padded_input)

if mode == 'ecb':
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_input) + encryptor.finalize()
    print(ct)
    print('encrypted with ecb mode')
elif mode == 'cbc':
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_input) + encryptor.finalize()
    print(ct)
    print('encrypted with cbc mode')
    print('with cbc mode') 
elif mode == 'gcm':
    cipher = Cipher(algorithms.AES(key),modes.GCM(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_input) + encryptor.finalize()
    with open (dir_path.joinpath(args.gcm_arg),'wb') as f:
        f.write(encryptor.tag)
        print(encryptor.tag)
    print('Encrypted GCM File Created')
else: 
    print('invalid mode')

with open (dir_path.joinpath(args.out),'wb') as f:
    f.write(ct)
    print('Encrypted File Created')