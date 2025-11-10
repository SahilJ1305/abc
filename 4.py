import hashlib

print("=== MD5 Hash Generator ===")
print("Type 'exit' to quit.\n")

while True:
    text = input("Enter text: ")
    if text.lower() == "exit":
        print("\nExiting...")
        break

    # Create MD5 hash object
    md5_hash = hashlib.md5(text.encode())

    # Convert to hexadecimal format
    digest = md5_hash.hexdigest()

    print("MD5 Hash:", digest, "\n")
