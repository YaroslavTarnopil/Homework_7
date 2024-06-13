import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Group, Teacher, Subject, Grade

# Конфігурація бази даних
DATABASE_URL = "postgresql+psycopg2://postgres:mypassword123@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def create_teacher(name):
    teacher = Teacher(name=name)
    session.add(teacher)
    session.commit()
    print(f"Створено вчителя з іменем '{name}'")

def list_teachers():
    teachers = session.query(Teacher).all()
    for teacher in teachers:
        print(f"ID: {teacher.id}, Name: {teacher.name}")

def update_teacher(teacher_id, name):
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    if teacher:
        teacher.name = name
        session.commit()
        print(f"Оновлено вчителя з ID {teacher_id} на '{name}'")
    else:
        print(f"Вчителя з ID {teacher_id} не знайдено")

def remove_teacher(teacher_id):
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    if teacher:
        session.delete(teacher)
        session.commit()
        print(f"Видалено вчителя з ID {teacher_id}")
    else:
        print(f"Вчителя з ID {teacher_id} не знайдено")

# Парсер аргументів командного рядка
parser = argparse.ArgumentParser(description="CLI програма для CRUD операцій з базою даних")
parser.add_argument("--action", "-a", choices=['create', 'list', 'update', 'remove'], required=True, help="Операція для виконання (create, list, update, remove)")
parser.add_argument("--model", "-m", choices=['Student', 'Group', 'Teacher', 'Subject', 'Grade'], required=True, help="Модель для виконання операції")

# Аргументи для кожної операції CRUD
if parser.parse_known_args()[0].model == "Teacher" and parser.parse_known_args()[0].action == "create":
    parser.add_argument("--name", help="Ім'я вчителя", required=True)
elif parser.parse_known_args()[0].model == "Teacher" and parser.parse_known_args()[0].action == "update":
    parser.add_argument("--id", type=int, help="ID вчителя для оновлення", required=True)
    parser.add_argument("--name", help="Нове ім'я вчителя", required=True)
elif parser.parse_known_args()[0].model == "Teacher" and parser.parse_known_args()[0].action == "remove":
    parser.add_argument("--id", type=int, help="ID вчителя для видалення", required=True)

args = parser.parse_args()

# Виконання операцій відповідно до введених аргументів
if args.model == "Teacher":
    if args.action == "create":
        create_teacher(args.name)
    elif args.action == "list":
        list_teachers()
    elif args.action == "update":
        update_teacher(args.id, args.name)
    elif args.action == "remove":
        remove_teacher(args.id)

# Закриття сесії
session.close()
