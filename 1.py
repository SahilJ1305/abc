# Cipher Implementations: Playfair, Vigenère, Columnar, Rail Fence

import math

# ----------------- PLAYFAIR CIPHER -----------------
def generate_playfair_key_matrix(key):
    key = key.replace("J", "I").upper()
    matrix = []
    used = []
    for c in key:
        if c not in used and c.isalpha():
            used.append(c)
    for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c not in used:
            used.append(c)
    for i in range(5):
        matrix.append(used[i*5:(i+1)*5])
    return matrix

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return i, j
    return None

def playfair_encrypt(text, key):
    matrix = generate_playfair_key_matrix(key)
    text = text.replace("J", "I").upper().replace(" ", "")
    i = 0
    pairs = []
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            b = 'X'
            i += 1
        else:
            i += 2
        pairs.append((a, b))
    cipher = ""
    for a, b in pairs:
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)
        if r1 == r2:
            cipher += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2:
            cipher += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:
            cipher += matrix[r1][c2] + matrix[r2][c1]
    return cipher

def playfair_decrypt(cipher, key):
    matrix = generate_playfair_key_matrix(key)
    cipher = cipher.upper().replace(" ", "")
    text = ""
    for i in range(0, len(cipher), 2):
        a, b = cipher[i], cipher[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)
        if r1 == r2:
            text += matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
        elif c1 == c2:
            text += matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
        else:
            text += matrix[r1][c2] + matrix[r2][c1]
    return text

# ----------------- VIGENERE CIPHER -----------------
def vigenere_encrypt(text, key):
    text = text.upper().replace(" ", "")
    key = key.upper()
    key = (key * (len(text)//len(key)+1))[:len(text)]
    cipher = ""
    for t, k in zip(text, key):
        cipher += chr(((ord(t)-65 + ord(k)-65) % 26) + 65)
    return cipher

def vigenere_decrypt(cipher, key):
    cipher = cipher.upper().replace(" ", "")
    key = key.upper()
    key = (key * (len(cipher)//len(key)+1))[:len(cipher)]
    text = ""
    for c, k in zip(cipher, key):
        text += chr(((ord(c)-65 - (ord(k)-65)) % 26) + 65)
    return text

# ----------------- COLUMNAR CIPHER -----------------
def columnar_encrypt(text, key):
    text = text.replace(" ", "")
    key_order = sorted(list(key))
    col = len(key)
    row = math.ceil(len(text)/col)
    fill = row * col - len(text)
    text += "_" * fill
    matrix = [list(text[i:i+col]) for i in range(0, len(text), col)]
    cipher = ""
    for k in key_order:
        col_index = key.index(k)
        for r in range(row):
            cipher += matrix[r][col_index]
    return cipher

def columnar_decrypt(cipher, key):
    col = len(key)
    row = math.ceil(len(cipher)/col)
    key_order = sorted(list(key))
    matrix = [['']*col for _ in range(row)]
    index = 0
    for k in key_order:
        col_index = key.index(k)
        for r in range(row):
            matrix[r][col_index] = cipher[index]
            index += 1
    text = "".join(["".join(r) for r in matrix]).replace("_", "")
    return text

# ----------------- RAIL FENCE CIPHER -----------------
def rail_fence_encrypt(text, rails):
    text = text.replace(" ", "")
    fence = [['\n' for i in range(len(text))] for j in range(rails)]
    dir_down = False
    row, col = 0, 0
    for i in range(len(text)):
        if row == 0 or row == rails-1:
            dir_down = not dir_down
        fence[row][col] = text[i]
        col += 1
        row += 1 if dir_down else -1
    cipher = ""
    for r in range(rails):
        for c in range(len(text)):
            if fence[r][c] != '\n':
                cipher += fence[r][c]
    return cipher

def rail_fence_decrypt(cipher, rails):
    cipher = cipher.replace(" ", "")
    fence = [['\n' for i in range(len(cipher))] for j in range(rails)]
    dir_down = None
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == rails - 1:
            dir_down = False
        fence[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1
    index = 0
    for i in range(rails):
        for j in range(len(cipher)):
            if fence[i][j] == '*' and index < len(cipher):
                fence[i][j] = cipher[index]
                index += 1
    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == rails - 1:
            dir_down = False
        if fence[row][col] != '*':
            result.append(fence[row][col])
            col += 1
        row += 1 if dir_down else -1
    return "".join(result)

# ----------------- MAIN MENU -----------------
def main():
    print("\n==== CIPHER PROGRAM ====")
    print("1. Playfair Cipher")
    print("2. Vigenere Cipher")
    print("3. Columnar Cipher")
    print("4. Rail Fence Cipher")
    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        text = input("Enter text: ")
        key = input("Enter key: ")
        enc = playfair_encrypt(text, key)
        dec = playfair_decrypt(enc, key)
        print(f"\nEncrypted: {enc}")
        print(f"Decrypted: {dec}")
    elif choice == '2':
        text = input("Enter text: ")
        key = input("Enter key: ")
        enc = vigenere_encrypt(text, key)
        dec = vigenere_decrypt(enc, key)
        print(f"\nEncrypted: {enc}")
        print(f"Decrypted: {dec}")
    elif choice == '3':
        text = input("Enter text: ")
        key = input("Enter key: ")
        enc = columnar_encrypt(text, key)
        dec = columnar_decrypt(enc, key)
        print(f"\nEncrypted: {enc}")
        print(f"Decrypted: {dec}")
    elif choice == '4':
        text = input("Enter text: ")
        rails = int(input("Enter number of rails: "))
        enc = rail_fence_encrypt(text, rails)
        dec = rail_fence_decrypt(enc, rails)
        print(f"\nEncrypted: {enc}")
        print(f"Decrypted: {dec}")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
