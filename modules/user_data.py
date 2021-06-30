import json

user_token = ''
user_key = ''

'''
    Принцип такой, у программы есть 2 ключа, ключ пользователя и ключ шифрования и если мы запускаем программу впервые,
    то есть файла data.py c этими ключами нет, так что их нужно сгенирировать
'''
try:
    file = open('data.json', 'r', encoding='utf-8')
    data = json.load(file)
    file.close()
    user_token, user_key = data['user_token'], data['user_key']

except FileNotFoundError:
    import random
    import string
    from time import time


    def random_word(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))


    # Для токена пользователя возьму id железки, но так как я работаю на windows и не знаю сработает этот способ на Mac
    # или Linux то прокину ещё один try и если получу ошибку то просто сгенерирую рандомный
    try:
        import subprocess

        current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()

        if not current_machine_id:
            raise Exception('machine_id null')

        user_token = current_machine_id
    except:
        user_token = random_word(30) + str(time())

    user_key = random_word(20) + str(time())[-4:]

    file = open('data.json', 'w', encoding='utf-8')
    json.dump({
        'user_token': user_token,
        'user_key': user_key
    }, file)
    file.close()