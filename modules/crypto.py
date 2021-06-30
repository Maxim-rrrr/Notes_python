from pyDes import *
from modules.user_data import user_key


# Функция шифрования текста
def encrypt(text):
    return triple_des(user_key).encrypt(bytes(text, 'utf-8'), padmode=2)


# Функция дешифровки текста
def decrypt(code):
    return triple_des(user_key).decrypt(code, padmode=2).decode("utf-8", "replace")





