from pymongo import MongoClient
from loguru import logger

from config import config
from datetime import datetime

from modules.user_data import user_token
from modules.crypto import encrypt, decrypt

'''
    Здесь у меня кастомный класс для работы БД, основанный на классе MongoClient из pymongo
    
    Такая реализация позволяет получить объект уже с подключенной БД и набором собственных методов по работе с данными
    
    (А монго потому, что я JS разработчик)
'''


class DB(MongoClient):
    @logger.catch()
    def __init__(self, host=None):
        try:
            super().__init__(host, port=None, document_class=dict, tz_aware=None, connect=None, type_registry=None)
            logger.info('База данных подключена.')
        except:
            logger.error('Ошибка подключения БД.')

    # Добавление блокнота
    @logger.catch()
    def add_notebook(self) -> None:
        Notebook = self.notes_python_YL.notebooks
        try:
            Notebook.insert_one({
                'title': 'Новый блокнот',
                'user_token': user_token,
            })
            logger.info(f'Успешное добавление блокнота')
        except:
            logger.error('Ошибка добавления блокнота в БД')

    # Удаление блокнота
    @logger.catch()
    def del_notebook(self, id_notebook) -> None:
        Notebook = self.notes_python_YL.notebooks
        Note = self.notes_python_YL.notes
        try:
            Notebook.delete_one({
                '_id': id_notebook,
            })
            Note.delete_many({
                'id_notebook': str(id_notebook)
            })
            logger.info(f'Успешное удаление блокнота "{id_notebook}"')
        except:
            logger.error('Ошибка удаление блокнота в БД')

    # Получение всех блокнотов пользователя
    @logger.catch()
    def get_notebooks(self) -> list:
        Notebook = self.notes_python_YL.notebooks
        try:
            notebooks = Notebook.find({
                'user_token': user_token,
            })

            return list(notebooks)
        except:
            logger.error('Ошибка получения блокнотов из БД')

    # Изменение заголовка блокнота
    @logger.catch()
    def set_title_notebooks(self, id_notebook, title):
        Notebook = self.notes_python_YL.notebooks
        try:
            Notebook.update_one({'_id': id_notebook}, {'$set': {
                'title': title,
            }})
        except:
            logger.error('Ошибка получения блокнотов из БД')

    # Добавление заметки
    @logger.catch()
    def add_note(self, id_notebook) -> None:
        Note = self.notes_python_YL.notes
        try:
            Note.insert_one({
                'id_notebook': str(id_notebook),
                'title': encrypt('Новая заметка'),
                'text': encrypt('Текст новой заметки'),
                'date': datetime.now()
            })

            logger.info(f'Успешное добавление заметки')
        except:
            logger.error('Ошибка добавление заметки в БД')

    # Удаление заметки
    @logger.catch()
    def del_note(self, id_note) -> None:
        Note = self.notes_python_YL.notes
        try:
            Note.delete_one({
                '_id': id_note,
            })
            logger.info(f'Успешное удаление заметки "{id_note}"')
        except:
            logger.error('Ошибка удаление заметки в БД')

    # Сохранение заметки
    @logger.catch()
    def save_note(self, id_note, title, text):
        Note = self.notes_python_YL.notes
        try:
            note = Note.find_one({
                '_id': id_note
            })

            if note:
                Note.update_one({'_id': id_note}, {'$set': {
                    'title': encrypt(title),
                    'text': encrypt(text),
                    'date': datetime.now()
                }})

                note = Note.find_one({
                    '_id': id_note
                })

                return dict(note)

            return False
        except:
            logger.error('Ошибка сохранения заметки в БД')
            return False

    # Получение заметок определённого блокнота
    @logger.catch()
    def get_note(self, id_notebook) -> list:
        Note = self.notes_python_YL.notes
        try:
            notes = Note.find({
                'id_notebook': str(id_notebook),
            })

            notes = list(notes)

            for note in notes:
                note['title'] = decrypt(note['title'])
                note['text'] = decrypt(note['text'])

            return notes
        except:
            logger.error('Ошибка получения блокнотов из БД')


database = DB(config['mongo_connect'])
