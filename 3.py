from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Generate RSA keys (once)
key = RSA.generate(1024)
public_key = key.publickey()
cipher_rsa = PKCS1_OAEP.new(public_key)
decipher_rsa = PKCS1_OAEP.new(key)

print("=== RSA Encryption & Decryption ===")
print("Type 'exit' to quit.\n")

while True:
    msg = input("Enter message to encrypt: ")
    if msg.lower() == "exit":
        print("\nExiting... Goodbye! 👋")
        break

    # Encrypt
    encrypted = cipher_rsa.encrypt(msg.encode())
    encoded = base64.b64encode(encrypted).decode()
    print("Encrypted:", encoded)

    # Decrypt
    decoded = base64.b64decode(encoded)
    decrypted = decipher_rsa.decrypt(decoded).decode()
    print("Decrypted:", decrypted, "\n")
