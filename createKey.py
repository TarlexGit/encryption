import hashlib


myArr = bytearray()
password = 'mypassword'.encode()
key = hashlib.sha256(password).digest()

with open('key.bin', 'wb') as f:
    f.write(myArr)
    f.write(key)