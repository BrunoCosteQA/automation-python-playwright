import uuid
import random
import string

def generate_uuid():
    uid = uuid.uuid4()
    return uid

def generate_random_code(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))