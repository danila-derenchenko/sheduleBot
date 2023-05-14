from peewee import *

db = SqliteDatabase('data.db')

class People(Model):
    id = IntegerField(primary_key=True)                # ID

    user_id = IntegerField(unique=True, null=False)    # ID пользователя

    faculty_id = IntegerField(default=0)               # id факультета
    course = IntegerField(default=0)                   # номер курса
    #group = IntegerField(default=0)                   # номер группы

    action = TextField(default="None")                 # Действие у пользователя

    class Meta:
        database = db


class Note(Model):
    id = IntegerField(primary_key=True)          # ID

    date = IntegerField()                        # Время добавления записи
    date_push = IntegerField()                   # Время последнего пуша
    retry = IntegerField(default=3600)           # Время через которое надо повторять пуш (1 hour - default)

    user_id = IntegerField()            # ID пользователя, создавшего запись
    subject = TextField()               # Предмет занятия
    text = TextField()                  # Описание домашки
    done = BooleanField(default=False)  # Выполнена ли домашка

    class Meta:
        database = db


People.create_table()
Note.create_table()
