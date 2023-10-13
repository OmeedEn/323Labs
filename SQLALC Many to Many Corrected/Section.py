from orm_base import Base
from IntrospectionFactory import IntrospectionFactory
from db_connection import engine
from sqlalchemy import Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy.types import Time
from Course import Course # be careful of import?
from constants import START_OVER, INTROSPECT_TABLES, REUSE_NO_INTROSPECTION

import SectionClass as SC

introspection_type = IntrospectionFactory().introspection_type

if introspection_type == START_OVER or introspection_type == REUSE_NO_INTROSPECTION:
    class Section(Base):
        __tablename__ = SC.__tablename__
        course: Mapped["Course"] = SC.course
        departmentAbbreviation: Mapped[str] = SC.departmentAbbreviation
        courseNumber: Mapped[int] = SC.courseNumber
        sectionNumber: Mapped[int] = SC.sectionNumber
        semester: Mapped[str] = SC.semester
        sectionYear: Mapped[int] = SC.sectionYear
        building: Mapped[str] = SC.building
        room: Mapped[int] = SC.room
        schedule: Mapped[str] = SC.schedule
        startTime: Mapped[Time] = SC.startTime
        instructor: Mapped[str] = SC.instructor

        __table_args__ = SC.__table_args__

        def __init__(self, course: Course, sectionNumber: int, semester: str, sectionYear: int, building: str,
                     room: int, schedule: str, startTime: Time, instructor: str):
            # self.departmentAbbreviation = departmentAbbreviation
            # self.courseNumber = courseNumber
            self.set_course(course)
            self.sectionNumber = sectionNumber
            self.semester = semester
            self.sectionYear = sectionYear
            self.building = building
            self.room = room
            self.schedule = schedule
            self.startTime = startTime
            self.instructor = instructor

elif introspection_type == INTROSPECT_TABLES:
    class Section(Base):
        __table__ = Table(SC.__tablename__, Base.metadata, autoload_with=engine)
        course: Mapped["Course"] = SC.course
        """include the name conversion and relationships """
        departmentAbbreviation: Mapped[str] = column_property(__table__.c.department_abbreviation)
        courseNumber: Mapped[str] = column_property(__table__.c.course_number)
        sectionNumber: Mapped[str] = column_property(__table__.c.section_number)
        sectionYear: Mapped[str] = column_property(__table__.c.section_year)
        startTime: Mapped[str] = column_property(__table__.c.start_time)

        def __init__(self, course: Course, sectionNumber: int, semester: str, sectionYear: int, building: str,
                     room: int, schedule: str, startTime: Time, instructor: str):
            # self.departmentAbbreviation = departmentAbbreviation
            # self.courseNumber = courseNumber
            self.set_course(course)
            self.sectionNumber = sectionNumber
            self.semester = semester
            self.sectionYear = sectionYear
            self.building = building
            self.room = room
            self.schedule = schedule
            self.startTime = startTime
            self.instructor = instructor


setattr(Section, '__str__', SC.__str__)
setattr(Section, 'set_course', SC.set_course)
