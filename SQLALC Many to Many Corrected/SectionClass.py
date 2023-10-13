from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, CheckConstraint
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Course import Course
from sqlalchemy.types import Time

__tablename__ = "sections"
course: Mapped["Course"] = relationship(back_populates="sections")
departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', String(10),
                                                    primary_key=True)
courseNumber: Mapped[int] = mapped_column('course_number', Integer,
                                          primary_key=True)
sectionNumber: Mapped[int] = mapped_column('section_number', Integer,
                                           primary_key=True)
#Fall, Spring, Winterm Summer I, Summer II -->
semester: Mapped[str] = mapped_column('semester', String(10),
                                      CheckConstraint("semester IN ('Fall', 'Spring', 'Winter', 'Summer I', "
                                                      "'Summer II')", name="sections_semester_values_check"),
                                      nullable=False, primary_key=True)
sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False,
                                         primary_key=True)
#{VEC, ECS, EN2, EN3, EN4, ET, SSPA} -->
building: Mapped[str] = mapped_column('building', String(6),
                                      CheckConstraint("building IN('VEC', 'ECS', 'EN2', 'EN3', 'EN4', 'ET', 'SSPA')",
                                      name ="sections_building_values_check"), nullable=False)
room: Mapped[int] = mapped_column('room', Integer, nullable=False)
#MW, TuTh, MWF, F, S -->
schedule: Mapped[str] = mapped_column('schedule', String(6),
                                      CheckConstraint("schedule IN('MW', 'TuTh', 'MWF', 'F', 'S')",
                                                      name="sections_schedule_values_check"))
startTime: Mapped[Time] = mapped_column('start_time', Time, nullable=False)
instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)

#Primary key: {department_abbreviation, course_number, section_number, section_year, semester}

__table_args__ = (UniqueConstraint("section_year", "semester", "schedule", "start_time", "building", "room", name="sections_uk_01"),
                  UniqueConstraint("section_year", "semester", "schedule", "start_time", "instructor", name="sections_uk_02"),
                  ForeignKeyConstraint([departmentAbbreviation, courseNumber],
                                       [Course.departmentAbbreviation, Course.courseNumber]))

def set_course(self, course: Course):
    """
    Accept a new department withoug checking for any uniqueness.
    I'm going to assume that either a) the caller checked that first
    and/or b) the database will raise its own exception.
    :param department:  The new department for the course.
    :return:            None
    """
    self.course = course
    self.departmentAbbreviation = course.departmentAbbreviation
    self.courseNumber = course.courseNumber


def __str__(self):
    return f"Department Abbreviation: {self.departmentAbbreviation} Course Number: {self.courseNumber} Section Number: {self.sectionNumber} \n" \
           f"Year: {self.sectionYear} Semester: {self.semester} Building: {self.building} Room: {self.room}\n " \
           f"Schedule: {self.schedule} Start Time: {self.startTime} Instructor: {self.instructor}\n"

