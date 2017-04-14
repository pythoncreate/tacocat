import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

from peewee import *

DATABASE = SqliteDatabase('taco.db')

class User(UserMixin,Model):
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    def get_tacos(self):
        return Taco.select().where(Taco.user == self)


    @classmethod
    def create_user(cls, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")

class Taco(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        rel_model = User,
        related_name = 'tacos'
    )
    protein = TextField()
    cheese = BooleanField(default=False)
    shell = TextField()
    extras = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)

def initialize():
    DATABASE.get_conn()
    DATABASE.create_tables([User, Taco], safe=True)
    DATABASE.close()