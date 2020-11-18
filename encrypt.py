import os, random, struct
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from base64 import b64decode 


def encrypt_file(key, in_filename, out_filename=None, init_vector=None, chunksize=64*1024): 
    check_encrypt_sign = 0
    try: 
        os.path.getsize(in_filename)
        in_filename.split("_")[1]
    except IndexError: 
        check_encrypt_sign = 1  
    except FileNotFoundError: 
        return print("File \"{f}\" not found".format(f =in_filename))
     
    if check_encrypt_sign == 0:
        print("0")
        return
    else:
        print("1")
    
    if not out_filename:
        out_filename = in_filename + '.enc'
    
    if not init_vector:
        init_vector = get_random_bytes(AES.block_size)
        print("init_vector => ", init_vector)
        
    
    print('iv ---- ', init_vector)
    encryptor = AES.new(key, AES.MODE_CBC, init_vector)
    filesize = os.path.getsize(in_filename)
    
    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile: 
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(init_vector) 

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0: 
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16) 
                outfile.write(encryptor.encrypt(chunk))
 

if __name__ == "__main__":
    """ create key bytes(16) and save to file for convenience"""
    iv = b'\xdb\xe4\x83r\x9f\x81\x96\x88d\x95\xaf\xcf\xf4\x1a\xde\xc6' 
    with open('key.bin', 'rb') as keyfile:
        key = keyfile.read()
        print(key)
        encrypt_file(key, "hello", init_vector=iv, out_filename="hello_enc")