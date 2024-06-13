from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Group, Teacher, Subject, Grade

# Конфігурація бази даних
DATABASE_URL = "postgresql+psycopg2://postgres:mypassword123@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    result = session.query(
        Student,
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade).group_by(Student).order_by(desc('average_grade')).limit(5).all()
    return result

# 2. Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_id):
    result = session.query(
        Student,
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade).filter(Grade.subject_id == subject_id).group_by(Student).order_by(desc('average_grade')).first()
    return result

# 3. Знайти середній бал у групах з певного предмета.
def select_3(subject_id):
    result = session.query(
        Group,
        func.avg(Grade.grade).label('average_grade')
    ).select_from(Group).join(Student).join(Grade).filter(Grade.subject_id == subject_id).group_by(Group).all()
    return result

# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    result = session.query(
        func.avg(Grade.grade).label('average_grade')
    ).first()
    return result

# 5. Знайти які курси читає певний викладач.
def select_5(teacher_id):
    result = session.query(
        Subject
    ).filter(Subject.teacher_id == teacher_id).all()
    return result

# 6. Знайти список студентів у певній групі.
def select_6(group_id):
    result = session.query(
        Student
    ).filter(Student.group_id == group_id).all()
    return result

# 7. Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_id, subject_id):
    result = session.query(
        Student,
        Grade
    ).join(Grade).filter(Student.group_id == group_id, Grade.subject_id == subject_id).all()
    return result

# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_id):
    result = session.query(
        func.avg(Grade.grade).label('average_grade')
    ).join(Subject).filter(Subject.teacher_id == teacher_id).first()
    return result

# 9. Знайти список курсів, які відвідує певний студент.
def select_9(student_id):
    result = session.query(
        Subject
    ).join(Grade).filter(Grade.student_id == student_id).group_by(Subject).all()
    return result

# 10. Список курсів, які певному студенту читає певний викладач.
def select_10(student_id, teacher_id):
    result = session.query(
        Subject
    ).join(Grade).filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id).group_by(Subject).all()
    return result

# Закриття сесії
session.close()

# Використання функцій для тестування
if __name__ == "__main__":
    print(select_1())
    print(select_2(1))
    print(select_3(1))
    print(select_4())
    print(select_5(1))
    print(select_6(1))
    print(select_7(1, 1))
    print(select_8(1))
    print(select_9(1))
    print(select_10(1, 1))
   