from orm_base import Base
from IntrospectionFactory import IntrospectionFactory
from db_connection import engine
from sqlalchemy import Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from typing import List  # Use this for the list of courses offered by the department
from constants import START_OVER, INTROSPECT_TABLES, REUSE_NO_INTROSPECTION

"""I'm defining my attributes and functions in another file as something of an
experiment.  I have to do virtually the same class definition regardless whether the
class is the product of introspection or I define it from scratch since I'm going to
override many of the names (to conform to our naming standards) as well as making
the relationship between Department and Course bidirectional, which is not the 
default mapping that introspection gives me."""
import DepartmentClass as DC

# Find out whether we're introspecting or recreating.
introspection_type = IntrospectionFactory().introspection_type

if introspection_type == START_OVER or introspection_type == REUSE_NO_INTROSPECTION:            # Define the entity from scratch

    class Department(Base):
        """An organization within a particular college within a university.  Each
        department offers one or more major fields of study to its students, and
        within each major, some number of courses.  Each course is offered on
        a regular basis as a scheduled section of a given course.

        Note, this is just a shell of the Department class.  There are additional
        columns needed, but this is enough to demonstrate one-to-many relationships."""
        __tablename__ = DC.__tablename__
        abbreviation: Mapped[str] = DC.abbreviation
        """This is a bi-directional relationship.  The Department class manages
        a list of Courses, and the Course class manages an OO reference to the
        "owning" Department.
        
        The Course referenced here is a string because the Course.py file 
        imports Departments.py.  If I try to import Course.py here, I'll set up
        a cyclic import loop and Python will not be able to interpret either of
        those class definition files."""
        courses: Mapped[List["Course"]] = DC.courses
        name: Mapped[str] = DC.name
        chairName: Mapped[str] = DC.chairName
        building: Mapped[str] = DC.building
        office: Mapped[int] = DC.office
        description: Mapped[str] = DC.description
        # __table_args__ can best be viewed as directives that we ask SQLAlchemy to
        # send to the database.  In this case, that we want two separate uniqueness
        # constraints (candidate keys).
        __table_args__ = DC.__table_args__

        """The __init__ function appears to be special in SQLAlchemy.  I'm unable to 
        leave that out when the class is initially declared, and then add it in afterwards.
        So I'm defining the exact same __init__ method both for the start over as well
        as the introspection case just to get past this interesting issue and move on."""

        def __init__(self, name: str, abbreviation: str, chair_name: str, building: str, office: int, description: str):
            self.name = name
            self.abbreviation = abbreviation
            self.chairName = chair_name
            self.building = building
            self.office = office
            self.description = description
elif introspection_type == INTROSPECT_TABLES:
    # We need to connect to the database to introspect the table.  So I'm getting that done
    # now, rather than in main.  Connection is a singleton factory of sorts.
    class Department(Base):
        # Creating the Table object does the introspection.  Basically, __table__
        # allows SQLAlchemy to copy the metadata from the Table object into Base.metadata.
        __table__ = Table(DC.__tablename__, Base.metadata, autoload_with=engine)
        # The uniqueness constraint that I explicitly define for the START_OVER approach is already
        # defined, so I don't need it here, so no __table_args__ needed.  The same consideration
        # applies to a foreign key constraint with multiple columns in the parent's primary key.

        # The courses list will not get created just from introspecting the database, so I'm doing that here.
        courses: Mapped[List["Course"]] = DC.courses
        # I'm not actually overriding the attribute name here, I just want to see if I can do it.
        # The __table__ attribute refers to the Table object that we created by introspection.
        # More on metadata: https://docs.sqlalchemy.org/en/20/core/metadata.html
        chairName: Mapped[str] = column_property(__table__.c.chair_name)
        abbreviation: Mapped[str] = column_property(__table__.c.abbreviation)

        def __init__(self, name: str, abbreviation: str, chair_name: str, building: str, office: int, description: str):
            self.abbreviation = abbreviation
            self.name = name
            self.chairName = chair_name
            self.building = building
            self.office = office
            self.description = description

"""I tried to bring in __init__ from the imported code in each of these two (see below)
ways, and in both cases when I tried to use the __init__ constructor, it blew up with
an error telling me that Department has no attribute: _sa_instance_state which I
GUESS means that the the __init__ method was somehow not included in vital processing 
that SQLAlchemy does at the end of defining the class.  Pure guesswork on my part."""

"""I could have defined these methods in this file, and then used setattr to add them
to the Department class, but I figured that dividing it up this way made Department.py
a little less cluttered.  I'm still boggled that all of these methods are instance
methods, and they add to the existing class just fine.  Python is scary sometimes."""
setattr(Department, 'add_course', DC.add_course)
setattr(Department, 'remove_course', DC.remove_course)
setattr(Department, 'get_courses', DC.get_courses)
setattr(Department, '__str__', DC.__str__)
