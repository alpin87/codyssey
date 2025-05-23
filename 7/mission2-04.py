def caesar_cipher_decode(target_text):
    cnt = 0

    print(target_text + ": " + str(cnt))

    for i in range(1, 26): 
        decoded_text = ""
        cnt += 1

        for c in target_text:
            if c == ' ':
                decoded_text += ' '
                continue

            if c.isupper():
                decoded_text += chr((ord(c) - i - 65) % 26 + 65)
                continue

            if c.islower():
                decoded_text += chr((ord(c) - i - 97) % 26 + 97)

        print(decoded_text + ": " + str(cnt))

        if cnt == 19:
            open("./result.txt", "w").write(decoded_text)

def read_password_file():
    return open("./password.txt", "r").read()

def main():
    target_text = read_password_file()
    print(caesar_cipher_decode(target_text))

if __name__ == "__main__":
    main()