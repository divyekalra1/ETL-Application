from logging import makeLogRecord
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    'sqlite3://vippul:vippuljpswd@localhost@5432/alchemy', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
    grade = Column(String(50))


Base.metadata.create_all(engine)

"""entering data"""

student1 = Student(name="Jerin", age=27, grade="Fifth")
student2 = Student(name="Divye", age=20, grade="Second")
student3 = Student(name="Vippul", age=19, grade="Second")

session.add_all(student1, student2, student3)

session.commit()

"""reading data"""

students = session.query(Student)

for student in students:
    print(student.name, student.age, student.grade)

"""in order"""

students = session.query(Student).order_by(Student.name)
student_count = session.query(Student).filter(
    or_(Student.name == "Vippul", Student.name == "Anita")).count()

for student in student_count:
    print(student.name, student.age)

"""change"""
student = session.query(Student).filter(Student.name == "Vippul").first()
student.name = 'Kevin'
session.commit()


"""Delete"""
student = session.query(Student).filter(Student.name == "Kevin").first()
session.delete(student)
session.commit()
