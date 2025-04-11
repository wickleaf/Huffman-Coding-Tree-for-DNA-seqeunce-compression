import random
import string
def text_generator():
    pattern = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\n"
    random_part = ''.join(random.choices('!@#$%^&*()'+string.ascii_letters+string.digits, k=5000))

    with open('compressible.txt', 'w') as f:
        f.write(pattern * 28000)  # Repeating part
        f.write(random_part)      # Random part
text_generator()