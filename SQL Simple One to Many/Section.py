from orm_base import Base
from db_connection import engine
from IntrospectionFactory import IntrospectionFactory
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import Table
from Department import Department
from constants import START_OVER, REUSE_NO_INTROSPECTION, INTROSPECT_TABLES
from Course import Course
from sqlalchemy.types import Time
from sqlalchemy import create_engine, Column, Integer, String, CheckConstraint
table_name: str = "sections"

introspection_type = IntrospectionFactory().introspection_type
if introspection_type == START_OVER | introspection_type == REUSE_NO_INTROSPECTION:
    class Section(Base):
        __tablename__ = table_name

        """attributes"""
        department_abbreviation: Mapped[str] = mapped_column('description', String(10), nullable=False, primary_key=True)
        course_number: Mapped[int] = mapped_column('course_number', Integer, nullable=False, primary_key=True)
        section_number: Mapped[int] = mapped_column('section_number', Integer, nullable=False, primary_key=True)
        semester: Mapped[str] = mapped_column('semester', String(10), nullable=False, primary_key=True, foreignkey=True)


        section_year: Mapped[int] = mapped_column('section_year', Integer, nullable=False, primary_key=True) #from [0,11] + 1
        building: Mapped[str] = mapped_column('building', String(6), nullable=False)
        room: Mapped[int] = mapped_column('room', Integer, nullable=False)
        schedule: Mapped[str] = mapped_column('schedule', String(6), nullable=False)
        instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)
        start_time: Mapped[Time] = mapped_column('start_time', String(10), nullable=True) # time() function

        """uniqueness constraints"""

        __table_args__ = (UniqueConstraint("year", "semester", "schedule", "start_time", "building", "room", name="sections_uk_01"),
                          UniqueConstraint("year", "semester", "schedule", "start_time", "instructor", name="sections_uk_02"),
                          CheckConstraint(semester.in_(['Fall', 'Spring', 'Winter', 'Summer I', 'Summer II']), name='valid_semester_check'),
                          CheckConstraint(building.in_(["VEC", "ECS", "EN2", "EN3", "EN4", "ET", "SSPA"])),
                          CheckConstraint(schedule.in_(["MW", "TuTh", "MWF", "F", "S"])),
                          ForeignKeyConstraint([course_number, department_abbreviation],
                                               [Course.courseNumber, Course.departmentAbbreviation]))



        def __int__(self, department_abbreviation: str, course_number:str, section_number:str, semester:str, section_year:int,
                    building:str, room:int, schedule:str, instructor:str, start_time:Time):

            self.department_abbreviation = department_abbreviation
            self.course_number = course_number
            self.section_number = section_number
            self.semester = semester
            self.section_year = section_year
            self.building = building
            self.room = room
            self.schedule = schedule
            self.instructor = instructor
            self.start_time = start_time

elif introspection_type == INTROSPECT_TABLES:
    class Section(Base):
        __table__ = Table(table_name, Base.metadata, autoload_with=engine)
        departmentAbbreviation: Mapped[str] = column_property(__table__.c.department_abbreviation)
        sectionNumber: Mapped[str] = column_property(__table__.c.section_number)
        semester: Mapped[str] = column_property(__table__.c.semester)
        sectionYear: Mapped[int] = column_property(__table__.c.section_year)
        building: Mapped[str] = column_property(__table__.c.building)
        room: Mapped[int] = column_property(__table__.c.room)
        schedule: Mapped[str] = column_property(__table__.c.schedule)
        start_time: Mapped[Time] = column_property(__table__.c.start_time)
        instructor: Mapped[str] = column_property(__table__.c.instructor)
        courseNumber: Mapped[int] = column_property(__table__.c.course_number)
        course: Mapped['Course'] = relationship(back_populates="section")

        def init(self, course: Course, sectionNumber: int, semester: str, sectionYear: int,
                 building: str, room: int, schedule: str, startTime: Time, instructor: str):
            self.set_course(course)
            self.sectionNumber = sectionNumber
            self.semester = semester
            self.sectionYear = sectionYear
            self.building = building
            self.room = room
            self.schedule = schedule
            self.start_time = startTime
            self.instructor = instructor

def __str__(self):
    return f"Department Abbreviation: {self.department_abbreviation}, Course Number: {self.course_number}, " \
           f"Section Number: {self.section_number}, Semester: {self.semester}, Section Year: {self.section_year}," \
           f"Building: {self.building}, Room: {self.room}, Schedule: {self.schedule}, Instructor: {self.instructor}," \
           f"Start Time: {self.start_time}"
