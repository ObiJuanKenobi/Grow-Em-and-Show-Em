import bcrypt
from peewee import *

#db = MySQLDatabase(
#        'may1713_PrisonGardenApp',
#        host   = 'sddb.ece.iastate.edu',
#        port   = 3306,
#        user   = 'may1713',
#        passwd = 'gawrA75Nac!&')

db = SqliteDatabase('plants.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    user_id         = PrimaryKeyField()
    user_name       = CharField()
    user_pass       = CharField()
    user_first_name = CharField()
    user_last_name  = CharField()

class Course(BaseModel):
    course_id   = PrimaryKeyField()
    course_name = CharField()
    course_file = CharField()

class Lesson(BaseModel):
    lesson_id     = PrimaryKeyField()
    lesson_name   = CharField()
    lesson_course = ForeignKeyField(Course, related_name='lessons')
    lesson_file   = CharField()

db.connect()
db.create_tables([User, Course, Lesson])

pw = 'therealboss'
password = bcrypt.hashpw(pw, bcrypt.gensalt())
juan = User(user_name = 'juanvegas',
            user_pass = password, 
            user_first_name = 'Juan',
            user_last_name  = 'Venegas')
juan.save()

for user in User.select():
    print(user.user_id,
          user.user_name,
          user.user_pass,
          user.user_first_name,
          user.user_last_name)
    if bcrypt.checkpw(pw, user.user_pass.encode('utf-8')):
        print('Password matches')
    else:
        print('Password does not match')
