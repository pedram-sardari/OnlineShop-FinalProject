import random
import string


def generate_random_code(length=12):
    characters = string.ascii_uppercase + string.digits
    discount_code = ''.join(random.choices(characters, k=length))

    return discount_code
