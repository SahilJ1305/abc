from PIL import Image
import numpy as np
import hashlib

# 1️⃣ Helper Functions
def text_to_bits(text):
    """Convert string to bits"""
    bits = bin(int.from_bytes(text.encode(), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits_to_text(bits):
    """Convert bits back to string"""
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

# 2️⃣ Embed Watermark Function
def embed_watermark(image_path, watermark_text, output_path, key):
    """Embed cryptographic watermark into an image"""
    # Open image and convert to RGB
    img = Image.open(image_path).convert('RGB')
    arr = np.array(img)

    # Generate cryptographic hash from key + watermark
    hash_object = hashlib.sha256((key + watermark_text).encode())
    watermark_hash = hash_object.hexdigest()[:16]  # Use first 16 chars
    watermark_bits = text_to_bits(watermark_hash)

    # Flatten image array for easy embedding
    flat_arr = arr.flatten()

    # Embed watermark bits into LSBs
    for i, bit in enumerate(watermark_bits):
        flat_arr[i] = np.uint8((int(flat_arr[i]) & 0b11111110) | int(bit))

    # Reshape array and save watermarked image
    watermarked_arr = flat_arr.reshape(arr.shape)
    watermarked_img = Image.fromarray(watermarked_arr)
    watermarked_img.save(output_path)

    print(f"[INFO] Watermark embedded and saved to {output_path}")
    print(f"[INFO] Embedded Hash: {watermark_hash}")

# 3️⃣ Extract Watermark Function
def extract_watermark(watermarked_path, watermark_length=16):
    """Extract watermark from the image"""
    img = Image.open(watermarked_path).convert('RGB')
    arr = np.array(img)
    flat_arr = arr.flatten()

    extracted_bits = ''
    for i in range(watermark_length * 8):  # Each char = 8 bits
        extracted_bits += str(flat_arr[i] & 1)

    extracted_text = bits_to_text(extracted_bits)
    return extracted_text

# 4️⃣ Driver Code
if __name__ == "__main__":
    image_path = 'boat.jpg'  # your input image
    watermarked_path = 'watermarked_image.png'
    watermark_text = 'SAHIL_SECRET'
    secret_key = 'MySecureKey123'

    # Embed watermark
    embed_watermark(image_path, watermark_text, watermarked_path, secret_key)

    # Extract watermark
    extracted = extract_watermark(watermarked_path)
    print(f"[INFO] Extracted Watermark: {extracted}")
