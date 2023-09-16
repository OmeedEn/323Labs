from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column



class Department(Base):

    __tablename__ = "departments"  # Give SQLAlchemy th name of the table.

    """attributes"""
    name = mapped_column('name', String(80), nullable=False, primary_key=True)
    abbreviation = mapped_column('abbreviation', String(6), unique=True, nullable=False)
    chair_name = mapped_column('chair_name', String(80), unique=True, nullable=False)
    building = mapped_column('building', String(10), nullable=False)
    office = mapped_column('office', Integer, nullable=False)
    description = mapped_column('description', String(80), unique=True, nullable=False)



    __table_args__ = (UniqueConstraint("name", name="departments_uk_01"),
                      UniqueConstraint("abbreviation", name="departments_uk_02"),
                      UniqueConstraint("chair_name", name="departments_uk_03"),
                      UniqueConstraint("description", name="departments_uk_04"),
                      UniqueConstraint('building', 'office', name='building_office_check'))

    def __init__(self, name: str, abbreviation : str, chair_name : str, building : str, office : int, description : str):
        self.name = name
        self.abbreviation = abbreviation
        self.chair_name = chair_name
        self.building = building
        self.office = office
        self.description = description

    def __str__(self):
        return f"Name: {self.name}, Abbreviation: {self.abbreviation}, Chair Name: {self.chair_name}, " \
               f"Building: {self.building}, Office: {self.office}, Description: {self.description}"
