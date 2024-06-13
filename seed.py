import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Group, Teacher, Subject, Grade
from datetime import datetime, timedelta

# Конфігурація бази даних
DATABASE_URL = "postgresql+psycopg2://postgres:mypassword123@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Ініціалізація Faker
faker = Faker()

# Створення груп
groups = []
for _ in range(3):
    group = Group(name=faker.word())
    groups.append(group)
    session.add(group)
session.commit()

# Створення викладачів
teachers = []
for _ in range(5):
    teacher = Teacher(first_name=faker.first_name(), last_name=faker.last_name())
    teachers.append(teacher)
    session.add(teacher)
session.commit()

# Створення предметів
subjects = []
for _ in range(8):
    subject = Subject(name=faker.word(), teacher=random.choice(teachers))
    subjects.append(subject)
    session.add(subject)
session.commit()

# Створення студентів
students = []
for _ in range(50):
    student = Student(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        group=random.choice(groups)
    )
    students.append(student)
    session.add(student)
session.commit()

# Створення оцінок для студентів
grades = []
for student in students:
    for subject in subjects:
        for _ in range(random.randint(10, 20)):  # До 20 оцінок для кожного студента з усіх предметів
            grade = Grade(
                student=student,
                subject=subject,
                grade=random.uniform(1, 10),  # Оцінка від 1 до 10
                date_received=faker.date_between(start_date="-1y", end_date="today")
            )
            grades.append(grade)
            session.add(grade)
session.commit()

# Закриття сесії
session.close()

print("Database seeding completed successfully!")
