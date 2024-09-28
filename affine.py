import sys

def egcd(a, b):
    # Returns d, s, t where d = gcd(a, b) and d = a * s + b * t
    s, t, u, v = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        s, t, u, v = u, v, s - u * q, t - v * q
    #a = gcd
    return a, s, t

def encrypt(plain_text, a, b):
    gcd, s, t, = egcd(a, 26)
    if (1 < a < 25 and 0 <= b < 26 and gcd == 1):
        cipher_text = ""
        for char in plain_text:
            if char.isalpha():
                if char.isupper():
                    cipher_text += chr(((a * (ord(char) - 65) + b) % 26) + 65)
                else:
                    cipher_text += chr(((a * (ord(char) - 97) + b) % 26) + 97)
            else:
                cipher_text += char
        return cipher_text
    else:
        print(f"The key pair ({a}, {b}) is invalid, please select another key.")
        return False


def decrypt(cipher_text, a, b):
    pass

def decipher(cipher_text):
    pass




if __name__ == '__main__':
    inputs = sys.stdin.readline().strip().split()
    if inputs[0] == 'encrypt':
        print(encrypt(inputs[1], int(inputs[2]), int(inputs[3])))
    elif inputs[0] == 'decrypt':
        print(decrypt(inputs[1], int(inputs[2]), int(inputs[3])))
    elif inputs[0] == 'decipher':
        print(decipher(inputs[1]))


#1. encrypt / decrypt / decipher