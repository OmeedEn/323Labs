from orm_base import Base
from IntrospectionFactory import IntrospectionFactory
from db_connection import engine
from sqlalchemy import Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from typing import List  # Use this for the list of courses offered by the department
from constants import START_OVER, INTROSPECT_TABLES, REUSE_NO_INTROSPECTION
import Course

"""I'm defining my attributes and functions in another file as something of an
experiment.  I have to do virtually the same class definition regardless whether the
class is the product of introspection or I define it from scratch since I'm going to
override many of the names (to conform to our naming standards) as well as making
the relationship between Department and Course bidirectional, which is not the 
default mapping that introspection gives me."""
import DepartmentClass as DC

# Find out whether we're introspecting or recreating.
introspection_type = IntrospectionFactory().introspection_type

if introspection_type == START_OVER | introspection_type == REUSE_NO_INTROSPECTION: # Define the entity from scratch

    class Department(Base):
        """An organization within a particular college within a university.  Each
        department offers one or more major fields of study to its students, and
        within each major, some number of courses.  Each course is offered on
        a regular basis as a scheduled section of a given course.

        Note, this is just a shell of the Department class.  There are additional
        columns needed, but this is enough to demonstrate one-to-many relationships."""
        __tablename__ = DC.__tablename__
        name: Mapped[str] = DC.name
        abbreviation: Mapped[str] = DC.abbreviation
        chair_name: Mapped[str] = DC.chair_name
        building: Mapped[str] = DC.building
        office: Mapped[int] = DC.office
        description: Mapped[str] = DC.description
        courses: Mapped[List["Course"]] = DC.courses

        """This is a bi-directional relationship.  The Department class manages
        a list of Courses, and the Course class manages an OO reference to the
        "owning" Department.
        
        The Course referenced here is a string because the Course.py file 
        imports Departments.py.  If I try to import Course.py here, I'll set up
        a cyclic import loop and Python will not be able to interpret either of
        those class definition files."""
        # __table_args__ can best be viewed as directives that we ask SQLAlchemy to
        # send to the database.  In this case, that we want two separate uniqueness
        # constraints (candidate keys).

        """The __init__ function appears to be special in SQLAlchemy.  I'm unable to 
        leave that out when the class is initially declared, and then add it in afterwards.
        So I'm defining the exact same __init__ method both for the start over as well
        as the introspection case just to get past this interesting issue and move on."""

        def __init__(self, name: str, abbreviation: str, chair_name: str, building: str, office: int, description: str):
            self.name = name
            self.abbreviation = abbreviation
            self.chair_name = chair_name
            self.building = building
            self.office = office
            self.description = description

        def __str__(self):
            return f"Department name: {self.name}, abbreviation: {self.abbreviation}, chair name: {self.chair_name}\n" \
                   f"building: {self.building}, office: {self.office}, description: {self.description}"

elif introspection_type == INTROSPECT_TABLES:
    class Department(Base):

        table = Table(DC.__tablename__, Base.metadata, autoload_with=engine)
        courses: Mapped[List["Course"]] = DC.courses
        abbreviation: Mapped[str] = column_property(table.c.abbreviation)
        chairName: Mapped[str] = column_property(table.c.chair_name)

        def init(self, name: str, abbreviation: str, chairName: str, building: str, office: int, description: str):
            self.name = name
            self.abbreviation = abbreviation
            self.chairName = chairName
            self.building = building
            self.office = office
            self.description = description

setattr(Department, 'add_course', DC.add_course)
setattr(Department, 'remove_course', DC.remove_course)
setattr(Department, 'get_courses', DC.get_courses)
setattr(Department, 'str', DC.__str__)
