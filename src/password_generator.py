from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import randint


LOWERCASE = ascii_lowercase
UPPERCASE = ascii_uppercase
DIGITS = digits
SPECIAL_CHARS = punctuation


class Password_generator:
    @classmethod
    def generate(cls, length: int = 12) -> str:
        password = ""
        password += LOWERCASE[randint(0, 25)]
        while len(password) != length - 1:
            num = randint(0, 28)
            if num in range(5):
                password += LOWERCASE[randint(0, 25)]
            elif num in range(5, 10):
                password += UPPERCASE[randint(0, 25)]
            elif num in range(10, 15):
                password += DIGITS[randint(0, 9)]
            elif num in range(15, 20):
                password += SPECIAL_CHARS[randint(1, 31)]
            elif num in range(20, 29):
                password += " "
        password += LOWERCASE[randint(0, 25)]

        return password
