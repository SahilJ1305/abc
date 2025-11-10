#pip install cryptography

import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

def generate_keys(key_size: int = 2048):
    """Generate an RSA private/public key pair."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    public_key = private_key.public_key()
    return private_key, public_key

def sign_message(private_key, message: bytes) -> bytes:
    """Sign the message using RSA-PSS with SHA-256 and return raw signature bytes."""
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(public_key, message: bytes, signature: bytes) -> bool:
    """Verify the signature. Returns True if valid, False otherwise."""
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

def pem_keys(private_key, public_key):
    """Return PEM-encoded private and public keys as strings (PEM, UTF-8)."""
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem_private.decode('utf-8'), pem_public.decode('utf-8')

def main():
    print("=== RSA-PSS (SHA-256) Digital Signature Demo ===\n")

    # 1. Generate keys
    private_key, public_key = generate_keys(2048)

    # 2. Get message to sign
    text = input("Enter message to sign (or type 'exit'): ")
    if text.lower() == "exit":
        print("Exiting.")
        return
    message = text.encode('utf-8')

    # 3. Sign
    signature = sign_message(private_key, message)
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    print("\nDigital Signature (Base64):")
    print(signature_b64)

    # 4. Verify
    is_valid = verify_signature(public_key, message, signature)
    print("\nVerification result:", "✅ Signature is valid." if is_valid else "❌ Signature is invalid.")

    # 5. (Optional) Print keys in PEM format
    pem_priv, pem_pub = pem_keys(private_key, public_key)
    print("\nPrivate Key (PEM):\n", pem_priv)
    print("Public Key (PEM):\n", pem_pub)

if __name__ == "__main__":
    main()
