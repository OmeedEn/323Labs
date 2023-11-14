from orm_base import Base
from sqlalchemy import String, ForeignKeyConstraint, ForeignKey, Integer, Identity, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


# Note that I do NOT migrate in any other classes in Enrollment.  I had to do that
# to avoid a cyclic import situation where Section imports Enrollment and Enrollment
# imports Section.


class Enrollment(Base):
    """An agreement between the university and a student that allows that student
    to participate in a specific section."""
    __tablename__ = "enrollments"
    # Enrollment has 6 columns in its primary key.  Time for a surrogate.
    enrollmentId: Mapped[int] = mapped_column('enrollment_id', Integer, Identity(start=1, cycle=True),
                                              primary_key=True)
    section: Mapped["Section"] = relationship(back_populates="students")
    departmentAbbreviation: Mapped[str] = mapped_column("department_abbreviation",
                                                        nullable=False)
    courseNumber: Mapped[int] = mapped_column("course_number",
                                              nullable=False)
    sectionNumber: Mapped[int] = mapped_column("section_number",
                                               nullable=False)
    semester: Mapped[str] = mapped_column("semester", String(20),
                                          nullable=False)
    sectionYear: Mapped[int] = mapped_column("section_year", nullable=False)
    student: Mapped["Student"] = relationship(back_populates="sections")
    studentID: Mapped[int] = mapped_column("student_id", ForeignKey("students.student_id"),
                                           nullable=False, primary_key=True)
    # sectionID: Mapped[int] = mapped_column('section_id', ForeignKey("sections.section_id"),
    #                                        primary_key=True)
    type: Mapped[str] = mapped_column("type", String(50), nullable=False)
    __table_args__ = (UniqueConstraint("enrollment_id", name="enrollment_uk_01"),

        # UniqueConstraint("department_abbreviation", "course_number",
        #                                "section_number", "section_year", "semester",
        #                                "student_id", name="enrollment_uk_01"),
              ForeignKeyConstraint(["department_abbreviation", "course_number",
                                    "section_number", "semester", "section_year"],
                                   ["sections.department_abbreviation",
                                    "sections.course_number", "sections.section_number",
                                    "sections.semester", "sections.section_year"],
                                   name="enrollments_sections_fk_01"),)

    __mapper_args__ = {"polymorphic_identity": "enrollment",
                       "polymorphic_on": "type"}

    def __init__(self, section, student):
        self.section = section
        self.departmentAbbreviation = section.departmentAbbreviation
        self.courseNumber = section.courseNumber
        self.sectionNumber = section.sectionNumber
        self.semester = section.semester
        self.sectionYear = section.sectionYear
        self.student = student
        self.studentID = student.studentID

    def __str__(self):
        return f"Enrollment- section: {self.section} student: {self.student}"
