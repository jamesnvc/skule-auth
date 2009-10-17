import os
import string

def rand_string(n):
    x = [ ]
    while len(x) < n:
        y = os.urandom(1)
        if y in (string.letters+string.digits):
            x += y
    return ''.join(x)
