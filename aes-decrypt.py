from importlib.resources import contents
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import argparse

dir_path = Path("Add your path here")

parser = argparse.ArgumentParser()
parser.add_argument('-key', help='key file')
parser.add_argument('-IV', help='IV file')
parser.add_argument('-mode', help='mode')
parser.add_argument('-input','-in', help='input')
parser.add_argument('-out', help='output')
parser.add_argument('-gcm_arg', help='additional file')
args = parser.parse_args()

with open(args.key,'r') as f:
    key = f.read()
    print(key)
f.close()
key = bytes.fromhex(key)
print(key)
print(len(key))

mode = args.mode
print(mode)

if mode == 'cbc'or mode == 'gcm':
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

decrypted_msg = b''
if mode == 'ecb':
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    decrypted_msg = decryptor.update(inputmsg)
    print(decrypted_msg)
    print('decrpyted with ecb mode')
elif mode == 'cbc':
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_msg = decryptor.update(inputmsg)
    print(decrypted_msg)
    print('with cbc mode')
elif mode == 'gcm':
    with open(args.gcm_arg,'rb') as f:
        tag = f.read()
    print(key)
    f.close()
    cipher = Cipher(algorithms.AES(key),modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    decrypted_msg = decryptor.update(inputmsg) + decryptor.finalize()
else: 
    print('invalid mode')

unpadder = padding.PKCS7(128).unpadder()
data = unpadder.update(decrypted_msg)
print(data)
unpadded_msg = data + unpadder.finalize()
print(unpadded_msg)

with open (dir_path.joinpath(args.out),'wb') as f:
        f.write(unpadded_msg)
        print('Decrypted File Created')