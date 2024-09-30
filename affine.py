import sys
import string


def read_characters():
    with open("all_characters.txt", "r") as f:
        return f.read().strip()

def egcd(a, b):
    s, t, u, v = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        s, t, u, v = u, v, s - u * q, t - v * q
    return a, s, t

def encrypt(plain_text_file, output_file, a, b):
    all_chars = read_characters()
    n = len(all_chars)  

    g, _, _ = egcd(a, n)
    if (g != 1):
        print("Invalid key options.")
        return False

    cipher_text = ""

    plain_text = ""
    with open(plain_text_file, "r") as f:
        plain_text = f.read()
    for char in plain_text:
        if char in all_chars:
            index = all_chars.index(char)
            cipher_index = (a * index + b) % n
            cipher_text += all_chars[cipher_index]
        else:
            cipher_text += char  

    with open(output_file, "w") as f:
        f.write(cipher_text)
    
    return cipher_text

def decrypt(cipher_text_file, output_file, a, b):
    all_chars = read_characters()
    n = len(all_chars)  
    
    g, x, _ = egcd(a, n)
    if (g != 1):
        print("Invalid key options.")
        return False
    
    a_inv = x % n
    
    cipher_text = ""
    with open(cipher_text_file, "r") as f:
        cipher_text = f.read()
    plain_text = ""
    for char in cipher_text:
        if char in all_chars:
            index = all_chars.index(char)
            plain_index = (a_inv * (index - b)) % n
            plain_text += all_chars[plain_index]
        else:
            plain_text += char  
    
    with open(output_file, "w") as f:
        f.write(plain_text)

    return plain_text

def decipher_decrypt(ciphertext, a, b, all_chars):
    n = len(all_chars)
    
    g, x, _ = egcd(a, n)
    if g != 1:
        return None
    a_inv = x % n

    plain_text = ""
    for char in ciphertext:
        if char in all_chars:
            index = all_chars.index(char)
            plain_index = (a_inv * (index - b)) % n
            plain_text += all_chars[plain_index]
        else:
            plain_text += char
    return plain_text

def check_words(text, dictionary):
    text = text.lower().translate(str.maketrans("", "", string.punctuation)).split()
    valid_words = 0
    for word in text:
        if len(word) >= 3 and word in dictionary:  
            valid_words += 1
    return valid_words

def decipher(ciphertext_file, output_file, dictionary_file):
    all_chars = read_characters()
    n = len(all_chars)

    with open(dictionary_file, "r") as f:
        dictionary = set(word.strip().lower() for word in f.readlines())

    with open(ciphertext_file, "r") as f:
        ciphertext = f.read().strip()

    best_a, best_b, most_valid_words = 0, 0, 0
    best_decryption = ""

    for a in range(1, n):
        if egcd(a, n)[0] != 1:
            continue
        for b in range(n):
            decrypted_text = decipher_decrypt(ciphertext, a, b, all_chars)
            if decrypted_text is None:
                continue

            valid_words = check_words(decrypted_text, dictionary)

            if valid_words > most_valid_words:
                best_a, best_b = a, b
                most_valid_words = valid_words
                best_decryption = decrypted_text

    if best_a is not None and best_b is not None:
        with open(output_file, "w") as f:
            f.write(f"{best_a} {best_b}\nDECIPHERED MESSAGE:\n{best_decryption}")
    else:
        print("No valid pair found.")

if __name__ == '__main__':
    inputs = sys.stdin.readline().strip().split()
    if inputs[0] == 'encrypt':
        encrypt(inputs[1], inputs[2], int(inputs[3]), int(inputs[4]))
    elif inputs[0] == 'decrypt':
        decrypt(inputs[1], inputs[2], int(inputs[3]), int(inputs[4]))
    elif inputs[0] == 'decipher':
        decipher(inputs[1], inputs[2], inputs[3])
    else:
        print("Invalid input, please try again.")
        sys.exit(1)
