from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from pathlib import Path
import os

path = str(Path.home()) + '\\Desktop' + '\\PyScript'
def encrypt_file_aes(key, input_file, output_file):
    # Generate a random initialization vector (IV)
    iv = os.urandom(16)  # AES block size is 16 bytes
gi
    # Read the input file content
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Ensure the plaintext is padded to a multiple of 16 bytes
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    # Create an AES cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the padded plaintext
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    # Write IV and ciphertext to the output file
    with open(output_file, 'wb') as f:
        f.write(iv)
        f.write(ciphertext)


def check_key():
    key = input("please enter your type of AES encoding: 16, 24 or 32")  # AES key must be either 16, 24, or 32 bytes long
    if key == '16' or 16:
        return b'Sixteen byte key'
    elif key == '24' or 24:
        return b'Twenty-four byte key!!!'
    elif key == '32' or 32:
        return b'Thirty-two byte key!!!!!!!!!'


def main_encrypt(plaintext):
    key = check_key()  # AES key must be either 16, 24, or 32 bytes long
    input_file = os.path.join(path, plaintext)
    output_file = os.path.join(path, 'encrypted_file.txt')
    encrypt_file_aes(key, input_file, output_file)

def create_plaintext_file(filename, text):
    filename = path+filename
    with open(filename, 'wb') as f:
        f.write(text.encode('utf-8'))
    return str(filename)

def create_plaintext_file_from_file(filename):
    with open(path+filename, 'rb') as f:
        f.read()
    return str(filename)

def check_answer(answer):
    while answer != '1' and answer != '2':
        asnwer = input("incorrect input, please try again")
        if asnwer == '1' or asnwer == '2':
            return

if __name__ == '__main__':
    answer = input("Do you want encrypt text or file?\n\t1.text - enter yours text.\n\t2.file - enter the file name.\n")
    check_answer(answer)
    if answer == '1':
        text = input("please enter your Plaintext: ")
        plaintext = create_plaintext_file('plaintext.txt', text)
        main_encrypt(plaintext)
    elif answer == '2':
        create_file = input("do you want to create file or using exist one.\n\t1.create file\n\t2.using existing file")
        check_answer(create_file)
        if create_file == '1':
            text = input("please enter your Plaintext: ")
            plaintext = create_plaintext_file('plaintext.txt', text)
            main_encrypt(plaintext)
        if create_file == '2':
            filename = input("please enter the file that you want to encrypt: ")
            plaintxt = create_plaintext_file_from_file(filename)
            main_encrypt(plaintxt)

