# aes_algorithm_hex_output.py
# Encrypt and Decrypt text using AES Algorithm (CBC Mode)
# Requires: pip install pycryptodome

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

# ---------- AES Encryption Function ----------
def aes_encrypt(plaintext, key):
    # Convert to bytes
    data = plaintext.encode('utf-8')
    key_bytes = key.encode('utf-8')

    # Ensure correct key length (pad/truncate to 32 bytes)
    key_bytes = key_bytes.ljust(32, b'\0')[:32]

    # Generate random IV
    iv = get_random_bytes(16)

    # Create AES cipher
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)

    # Encrypt
    ciphertext = cipher.encrypt(pad(data, AES.block_size))

    # Return both IV and ciphertext
    return iv, ciphertext


# ---------- AES Decryption Function ----------
def aes_decrypt(iv, ciphertext, key):
    key_bytes = key.encode('utf-8')
    key_bytes = key_bytes.ljust(32, b'\0')[:32]

    # Create cipher and decrypt
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted.decode('utf-8')


# ---------- Main Program ----------
if __name__ == "__main__":
    print("=== AES Encryption & Decryption (CBC Mode) ===")

    # Take user input
    plaintext = input("\nEnter the plaintext to encrypt: ")
    key = input("Enter your secret key: ")

    # Encrypt
    iv, ciphertext = aes_encrypt(plaintext, key)

    # Format ciphertext as hex bytes (for display)
    hex_cipher = ' '.join([f"{b:02X}" for b in ciphertext])

    print("\nEncrypted text (Ciphertext):", hex_cipher)

    # Decrypt
    decrypted = aes_decrypt(iv, ciphertext, key)
    print("\nDecrypted text:", decrypted)
