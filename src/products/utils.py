import random
import string


def generate_random_code(letters=False, digits=True, length=8):
    if digits and letters:
        characters = string.ascii_uppercase + string.digits
    elif digits:
        characters = string.digits
    elif letters:
        characters = string.ascii_uppercase
    else:
        raise ValueError("At list one of the digits or letters must be True")
    discount_code = ''.join(random.choices(characters, k=length))
    return discount_code
