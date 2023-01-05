import random


def otp_generator(rand_from, rand_to):
    return str(random.randint(rand_from, rand_to))
