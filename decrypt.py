from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
import struct 
import binascii
import os


def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):  
    mode = AES.MODE_CBC 

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as f: 
        origsize = struct.unpack('<Q', f.read(struct.calcsize('Q')))[0]
        iv = f.read(16)
        decryptor = AES.new(key, mode, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = f.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)
        return "ok"

if __name__ == "__main__":
    file_name = 'hello_encode'
    with open('key.bin', 'rb') as keyfile:
        key = keyfile.read()
        print(key)
        decrypt_file(key, "hello_enc", out_filename="hello_dec")