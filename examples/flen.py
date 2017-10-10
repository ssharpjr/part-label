#! /usr/bin/env python3

files = ['setup.zpl', 'data1.zpl', 'data2.zpl']


def main():
    for file in files:
        with open(file) as f:
            data = f.read()
            words = data.split()
            characters = 0
            for word in words:
                characters += len(word)
            print(file + " has " + str(characters) + " characters.")


if __name__ == "__main__":
    main()
