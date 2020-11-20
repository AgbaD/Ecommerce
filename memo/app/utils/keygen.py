#!/usr/bin/python3
# Author:   @AgbaD | @agba_dr3

from random import choice
import sys

lst = ["b", "a", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
       "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
       "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
       "/", "[", "]", "$", "@", "!", "%", "&", "+", "?", "|", "~"]


def gen_key(x=None):
    secret_key = []
    if x:
        for j in range(int(x)):
            secret_key.append(choice(lst))
    else:
        for j in range(27):
            secret_key.append(choice(lst))

    secret_key = "".join(secret_key)
    return secret_key


if __name__ == "__main__":
    key = []
    try:
        if sys.argv[1]:
            for i in range(int(sys.argv[1])):
                key.append(choice(lst))
    except:
        for i in range(27):
            key.append(choice(lst))

    key = "".join(key)
    print(key)

