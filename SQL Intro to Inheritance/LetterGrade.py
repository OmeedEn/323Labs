from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import String, ForeignKeyConstraint, ForeignKey, Integer, Identity, UniqueConstraint, CheckConstraint
from orm_base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Enrollment import Enrollment

class LetterGrade(Enrollment):
    __tablename__ = 'letter_grade'

    # Assuming you want to use the same primary key as Enrollment for a one-to-one relationship
    letterGradeID: Mapped[int] = mapped_column('enrollment_id',
                                            ForeignKey("enrollments.enrollment_id",
                                                       ondelete="CASCADE"), primary_key=True)

    minSatisfactory: Mapped[str] = mapped_column("minSatisfactory", nullable=False)
                    #CheckConstraint("minSatisfactory in ('A', 'B', 'C', 'D', 'F')",
                                    #name="letterGrade_minSatisfactory_constraint"), nullable=False)
    __mapper_args__ = {"polymorphic_identity": "letter_grade"}
    __table_args__ = (CheckConstraint(minSatisfactory.in_(['A', 'B', 'C', 'D', 'F']), name='letter_grade_constraint'), )

    def __init__(self, section, student, grade):
        super().__init__(section, student)
        self.minSatisfactory = grade

    def __str__(self):
        return f"LetterGrade Enrollment: {super.__str__()}"
