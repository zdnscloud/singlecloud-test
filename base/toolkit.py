import random
import string

default_random_str_length = 8


def gen_random_str(length=default_random_str_length):
    return ''.join([random.choice(string.ascii_letters) for _ in range(length)])
