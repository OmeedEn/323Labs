import logging
from constants import *
from menu_definitions import menu_main, add_menu, delete_menu, list_menu, debug_select, introspection_select
from IntrospectionFactory import IntrospectionFactory
from db_connection import engine, Session
from datetime import time, datetime
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Department import Department
from Course import Course
from Major import Major
from Student import Student
from StudentMajor import StudentMajor
from Enrollment import Enrollment
from LetterGrade import LetterGrade
from PassFail import PassFail
from Section import Section
from Option import Option
from Menu import Menu
from datetime import time


def add(sess: Session):
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(sess: Session):
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(sess: Session):
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def add_department(session: Session):
    """
    Prompt the user for the information for a new department and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_abbreviation: bool = False
    unique_chairName: bool = False
    unique_building_and_office: bool = False
    unique_description: bool = False

    name: str = ''
    abbreviation: str = ''
    chairName: str = ''
    building: str = ''
    office: int = 0
    description: str = ''

    while not unique_abbreviation or not unique_name:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        chair = input("Department chair name--> ")
        building = input("Department building--> ")
        office = input("Department office--> ")
        description = input("Department description--> ")

        name_count: int = session.query(Department).filter(Department.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a department by that name.  Try again.")
        if unique_name:
            abbreviation_count = session.query(Department).filter(Department.abbreviation == abbreviation).count()
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print("We already have a department with that abbreviation.  Try again.")
            if unique_abbreviation:
                chair_count: int = session.query(Department).filter(Department.chairName == chair)
                unique_chairName = chair_count == 0
                if not unique_chairName:
                    print("We already have a department with that chair name. Try again.")
                if unique_chairName:
                    build_count: int = session.query(Department).filter(Department.building == building,
                                                                        Department.office == office).count()
                    unique_building_and_office = build_count == 0
                    if not unique_building_and_office:
                        print("We already have a department with that building and office. Try again.")
                    if unique_building_and_office:
                        description_count: int = session.query(Department).filter(
                            Department.description == description).count()
                        unique_description = description_count == 0
                        if not unique_description:
                            print("We already have a department with that description. Try again.")

    new_department = Department(abbreviation, name, chairName, building, office, description)
    session.add(new_department)


def add_course(session: Session):
    """
    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this course?")
    department: Department = select_department(sess)
    unique_number: bool = False
    unique_name: bool = False
    number: int = -1
    name: str = ''
    while not unique_number or not unique_name:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))
        name_count: int = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation,
                                                       Course.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            number_count = session.query(Course). \
                filter(Course.departmentAbbreviation == department.abbreviation,
                       Course.courseNumber == number).count()
            unique_number = number_count == 0
            if not unique_number:
                print("We already have a course in this department with that number.  Try again.")
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))
    course = Course(department, number, name, description, units)
    session.add(course)


def add_major(session: Session):
    """
    Prompt the user for the information for a new major and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this major?")
    department: Department = select_department(sess)
    unique_name: bool = False
    name: str = ''
    while not unique_name:
        name = input("Major name--> ")
        name_count: int = session.query(Major).filter(Major.departmentAbbreviation == department.abbreviation,
                                                      ).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a major by that name in that department.  Try again.")
    description: str = input('Please give this major a description -->')
    major: Major = Major(department, name, description)
    session.add(major)


def add_student(session: Session):
    """
    Prompt the user for the information for a new student and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_email: bool = False
    last_name: str = ''
    first_name: str = ''
    email: str = ''
    while not unique_email or not unique_name:
        last_name = input("Student last name--> ")
        first_name = input("Student first name-->")
        email = input("Student e-mail address--> ")
        name_count: int = session.query(Student).filter(Student.lastName == last_name,
                                                        Student.firstName == first_name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name.  Try again.")
        if unique_name:
            email_count = session.query(Student).filter(Student.email == email).count()
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that email address.  Try again.")
    new_student = Student(last_name, first_name, email)
    session.add(new_student)


def add_section(session):
    print("Which course offers this section?")
    course: Course = select_course(sess)
    unique_section_number: bool = False
    # for set of uk's i. no more than 1 section in same room at same time
    unique_room_set: bool = False
    # for set of uk's ii. never overbook instructor teaching 2 sections at same time
    unique_instructor_set: bool = False

    section_number: int = -1
    section_year: int = -1
    semester: str = ''
    schedule: str = ''
    startTime: time = time(0, 0, 0)
    building: str = ''
    room: int = -1
    instructor: str = ''

    while not unique_section_number or not unique_room_set or not unique_instructor_set:
        sectionNumber = int(input("Section number--> "))
        sectionYear = int(input("Section Year--> "))
        semester = input("Section semester--> ")
        schedule = input("Schedule--> ")
        startTimeHour = int(input("Section start time hour--> "))
        startTimeMinute = int(input("Section start time minute--> "))
        building = input("Section building--> ")
        room = int(input("Section room--> "))
        instructor = input("Section instructor--> ")

        valid_semester = True
        if semester not in ('Fall', 'Spring', 'Winter', 'Summer I', 'Summer II'):
            print("Invalid semester. Try again.")
            valid_semester = False
        valid_schedule = True
        if schedule not in ('MW', 'TuTh', 'MWF', 'F', 'S'):
            print("Invalid schedule. Try again.")
            valid_schedule = False
        valid_building = True
        if building not in ('VEC', 'ECS', 'EN2', 'EN3', 'EN4', 'ET', 'SSPA'):
            print("Invalid building. Try again.")
            valid_building = False

        if valid_semester or valid_schedule or valid_building:
            section_number_count: int = session.query(Section).filter(
                Section.departmentAbbreviation == course.departmentAbbreviation,
                Section.courseNumber == course.courseNumber,
                Section.sectionYear == sectionYear,
                Section.sectionNumber == sectionNumber,
                Section.semester == semester).count()
            unique_section_number = section_number_count == 0
            if not unique_section_number:
                print("We already have a section with that number for this course. Try again.")
            if unique_section_number:
                room_set_count: int = session.query(Section).filter(Section.sectionYear == sectionYear,
                                                                    Section.semester == semester,
                                                                    Section.schedule == schedule,
                                                                    Section.startTime == startTime,
                                                                    Section.building == building,
                                                                    Section.room == room).count()
                unique_room_set = room_set_count == 0
                if not unique_room_set:
                    print(
                        "We already have a section with the same year, semester, schedule, start time, and in the same room."
                        "Try again.")
                if unique_room_set:
                    instructor_set_count: int = session.query(Section).filter(Section.sectionYear == sectionYear,
                                                                              Section.semester == semester,
                                                                              Section.schedule == schedule,
                                                                              Section.startTime == startTime,
                                                                              Section.instructor == instructor).count()
                    unique_instructor_set = instructor_set_count == 0
                    if not unique_instructor_set:
                        print(
                            "We already have a section with the same year, semester, schedule, start time, taught by the same"
                            "instructor. Try again.")
        startTime = time(startTimeHour, startTimeMinute, 0)
        newSection = Section(course, sectionNumber, semester, sectionYear, building, room, schedule, startTime,
                             instructor)
        session.add(newSection)

#finished
def add_student_section(sess):
    student: Student = select_student(sess)
    section: Section = select_section(sess)
    is_enrolled = sess.query(Enrollment).join(Section).filter(
        Enrollment.student == student,
        Section.sectionID == Enrollment.sectionID,
        Section.departmentAbbreviation == section.departmentAbbreviation,
        Section.courseNumber == section.courseNumber,
        Section.sectionYear == section.sectionYear,
        Section.semester == section.semester).count() > 0
    while is_enrolled:
        print("That student is already enrolled in that course for the semester. Try again.")
        student = select_student(sess)
        section = select_section(sess)
        #constraint for surrogate key if student is already in a section for same course in same year/semester
        is_enrolled = sess.query(Enrollment).join(Section).filter(
            Enrollment.student == student,
            Section.sectionID == Enrollment.sectionID,
            Section.departmentAbbreviation == section.departmentAbbreviation,
            Section.courseNumber == section.courseNumber,
            Section.sectionYear == section.sectionYear,
            Section.semester == section.semester).count() > 0
    student.add_section(section)
    sess.add(student)
    sess.flush()

#finished
def add_section_student(sess):
    section: Section = select_section(sess)
    student: Student = select_student(sess)
    # constraint for surrogate key if section already has a student for same course in same year/semester
    is_enrolled = sess.query(Enrollment).join(Section).filter(
        Enrollment.student == student,
        Student.studentID == Enrollment.studentID,
        Section.departmentAbbreviation == section.departmentAbbreviation,
        Section.courseNumber == section.courseNumber,
        Section.sectionYear == section.sectionYear,
        Section.semester == section.semester).count() > 0
    while is_enrolled:
        print("That section already has that student enrolled in it for the semester. Try again.")
        section = select_section(sess)
        student = select_student(sess)
        is_enrolled = sess.query(Enrollment).join(Section).filter(
            Enrollment.student == student,
            Student.studentID == Enrollment.studentID,
            Section.departmentAbbreviation == section.departmentAbbreviation,
            Section.courseNumber == section.courseNumber,
            Section.sectionYear == section.sectionYear,
            Section.semester == section.semester).count() > 0
    section.add_student(student)
    sess.add(section)
    sess.flush()

def count_student_section(sess, student: Student, section: Section):
    """Count the number of Enrollment instances for a given student & section.
    :param  sess        The current session.
    :param  student     The enrolling student.
    :param  section     The section that we want to see whether that student is enrolled."""
    pk_count: int = sess.query(Enrollment).filter(
        Enrollment.departmentAbbreviation == section.departmentAbbreviation,
        Enrollment.courseNumber == section.courseNumber,
        Enrollment.sectionNumber == section.sectionNumber,
        Enrollment.sectionYear == section.sectionYear,
        Enrollment.semester == section.semester,
        Enrollment.studentID == student.studentID).count()
    return pk_count

def add_student_major(sess):
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    student_major_count: int = sess.query(StudentMajor).filter(StudentMajor.studentId == student.studentID,
                                                               StudentMajor.majorName == major.name).count()
    unique_student_major: bool = student_major_count == 0
    while not unique_student_major:
        print("That student already has that major.  Try again.")
        student = select_student(sess)
        major = select_major(sess)
    student.add_major(major)
    """The student object instance is mapped to a specific row in the Student table.  But adding
    the new major to its list of majors does not add the new StudentMajor instance to this session.
    That StudentMajor instance was created and added to the Student's majors list inside of the
    add_major method, but we don't have easy access to it from here.  And I don't want to have to 
    pass sess to the add_major method.  So instead, I add the student to the session.  You would
    think that would cause an insert, but SQLAlchemy is smart enough to know that this student 
    has already been inserted, so the add method takes this to be an update instead, and adds
    the new instance of StudentMajor to the session.  THEN, when we flush the session, that 
    transient instance of StudentMajor gets inserted into the database, and is ready to be 
    committed later (which happens automatically when we exit the application)."""
    sess.add(student)  # add the StudentMajor to the session
    sess.flush()

def add_student_PassFail(sess):
    """
    Add a student to a section as a pass/fail.
    :param sess: The current database connection.
    :return:    None
    """
    student: Student
    section: Section
    unique_student_section: bool = False
    while not unique_student_section:
        student = select_student(sess)
        section = select_section(sess)
        pk_count: int = count_student_section(sess, student, section)
        unique_student_section = pk_count == 0
        if not unique_student_section:
            print("That section already has that student enrolled in it.  Try again.")
    pass_fail = PassFail(section, student, datetime.now())
    sess.add(pass_fail)
    sess.flush()

def add_letter_grade(sess):
    student: Student
    section: Section
    unique_student_section: bool = False
    while not unique_student_section:
        grade: str = input("What is your grade?---> ")
        student = select_student(sess)
        section = select_section(sess)
        pk_count: int = count_student_section(sess, student, section)
        unique_student_section = pk_count == 0
        if not unique_student_section:
            print("That section already has that student enrolled in it. Try again.")
    letter_grade = LetterGrade(section, student, grade)
    sess.add(letter_grade)
    sess.flush()

def add_major_student(sess):
    major: Major = select_major(sess)
    student: Student = select_student(sess)
    student_major_count: int = sess.query(StudentMajor).filter(StudentMajor.studentId == student.studentID,
                                                               StudentMajor.majorName == major.name).count()
    unique_student_major: bool = student_major_count == 0
    while not unique_student_major:
        print("That major already has that student.  Try again.")
        major = select_major(sess)
        student = select_student(sess)
    major.add_student(student)
    """The major object instance is mapped to a specific row in the Major table.  But adding
    the new student to its list of students does not add the new StudentMajor instance to this session.
    That StudentMajor instance was created and added to the Major's students list inside of the
    add_student method, but we don't have easy access to it from here.  And I don't want to have to 
    pass sess to the add_student method.  So instead, I add the major to the session.  You would
    think that would cause an insert, but SQLAlchemy is smart enough to know that this major 
    has already been inserted, so the add method takes this to be an update instead, and adds
    the new instance of StudentMajor to the session.  THEN, when we flush the session, that 
    transient instance of StudentMajor gets inserted into the database, and is ready to be 
    committed later (which happens automatically when we exit the application)."""
    sess.add(major)  # add the StudentMajor to the session
    sess.flush()


def select_department(sess: Session) -> Department:
    """
    Prompt the user for a specific department by the department abbreviation.
    :param sess:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Enter the department abbreviation--> ")
        abbreviation_count: int = sess.query(Department). \
            filter(Department.abbreviation == abbreviation).count()
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation.  Try again.")
    return_department: Department = sess.query(Department). \
        filter(Department.abbreviation == abbreviation).first()
    return return_department


def select_course(sess: Session) -> Course:
    """
    Select a course by the combination of the department abbreviation and course number.
    Note, a similar query would be to select the course on the basis of the department
    abbreviation and the course name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = -1
    while not found:
        department_abbreviation = input("Department abbreviation--> ")
        course_number = int(input("Course Number--> "))
        name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                                    Course.courseNumber == course_number).count()
        found = name_count == 1
        if not found:
            print("No course by that number in that department.  Try again.")
    course = sess.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                       Course.courseNumber == course_number).first()
    return course


def select_student(sess) -> Student:
    """
    Select a student by the combination of the last and first.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    last_name: str = ''
    first_name: str = ''
    while not found:
        last_name = input("Student's last name--> ")
        first_name = input("Student's first name--> ")
        name_count: int = sess.query(Student).filter(Student.lastName == last_name,
                                                     Student.firstName == first_name).count()
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    student: Student = sess.query(Student).filter(Student.lastName == last_name,
                                                  Student.firstName == first_name).first()
    return student


def select_section(sess) -> Section:
    # prompt the user for a course
    # go to the list of sections within that course object and display the sections
    found: bool = False
    sectionYear = -1
    semester = ''
    schedule = ''
    instructor = ''
    while not found:
        sectionYear = int(input("Section section year--> "))
        semester = input("Section semester--> ")
        schedule = input("Section schedule--> ")
        instructor = input("Section instructor--> ")

        year_count: int = sess.query(Section).filter(Section.sectionYear == sectionYear,
                                                     Section.semester == semester,
                                                     Section.schedule == schedule,
                                                     Section.instructor == instructor).count()
        found = year_count == 1
        if not found:
            print("No section with those values for that course. Try again.")
    section = sess.query(Section).filter(Section.sectionYear == sectionYear,
                                         Section.semester == semester,
                                         Section.schedule == schedule,
                                         Section.instructor == instructor).first()
    print("Selected section:\n", section)
    return section


def select_major(sess) -> Major:
    """
    Select a major by its name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    name: str = ''
    while not found:
        name = input("Major's name--> ")
        name_count: int = sess.query(Major).filter(Major.name == name).count()
        found = name_count == 1
        if not found:
            print("No major found by that name.  Try again.")
    major: Major = sess.query(Major).filter(Major.name == name).first()
    return major

#finished
def delete_student(session: Session):
    """
    Prompt the user for a student to delete and delete them.
    :param session:     The current connection to the database.
    :return:            None
    """
    print("deleting a student")
    student = select_student(session)
    n_sections = session.query(Course).filter(Course.courseNumber == Student.studentID).count()
    if n_sections > 0:
        print(f"Sorry, this student is enrolled in {n_sections} sections. Delete them first, then try again.")
    else:
        session.delete(student)


def delete_department(session: Session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a department")
    department = select_department(session)
    n_courses = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f"Sorry, there are {n_courses} courses in that department.  Delete them first, "
              "then come back here to delete the department.")
    else:
        session.delete(department)


#finished
def delete_section(session: Session):
    print("deleting a section")
    section = select_section(session)
    n_enrollments = session.query(Enrollment).filter(Course.courseNumber == Section.sectionID).count()
    if n_enrollments > 0:
        print(f"Sorry, there are {n_enrollments} enrollments in that section. Delete them first, "
              f"then come back here to delete the section.")
    else:
        session.delete(section)

#unenroll student starting with student, finished
def delete_student_section(sess):
    print("deleting a student from a section")
    student: Student = select_student(sess)
    section: Section = select_section(sess)
    student.remove_section(section)

#unenroll student starting with section, finished
def delete_section_student(sess):
    print("deleting section from a student")
    section: Section = select_section(sess)
    student: Student = select_student(sess)
    section.remove_enrollment(student)


def delete_student_major(sess):
    """Undeclare a student from a particular major.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the student and the major that they no longer have.")
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    student.remove_major(major)


def delete_major_student(sess):
    """Remove a student from a particular major.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the major and the student who no longer has that major.")
    major: Major = select_major(sess)
    student: Student = select_student(sess)
    major.remove_student(student)


def list_department(session: Session):
    """
    List all departments, sorted by the abbreviation.
    :param session:     The connection to the database.
    :return:            None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    departments: [Department] = list(session.query(Department).order_by(Department.abbreviation))
    for department in departments:
        print(department)


def list_course(sess: Session):
    """
    List all courses currently in the database.
    :param sess:    The connection to the database.
    :return:        None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    courses: [Course] = list(sess.query(Course).order_by(Course.courseNumber))
    for course in courses:
        print(course)


def list_student(sess: Session):
    """
    List all Students currently in the database.
    :param sess:    The current connection to the database.
    :return:
    """
    students: [Student] = list(sess.query(Student).order_by(Student.lastName, Student.firstName))
    for student in students:
        print(student)


def list_major(sess: Session):
    """
    List all majors in the database.
    :param sess:    The current connection to the database.
    :return:
    """
    majors: [Major] = list(sess.query(Major).order_by(Major.departmentAbbreviation))
    for major in majors:
        print(major)


def list_student_major(sess: Session):
    """Prompt the user for the student, and then list the majors that the student has declared.
    :param sess:    The connection to the database
    :return:        None
    """
    student: Student = select_student(sess)
    recs = sess.query(Student).join(StudentMajor, Student.studentID == StudentMajor.studentId).join(
        Major, StudentMajor.majorName == Major.name).filter(
        Student.studentID == student.studentID).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}")


def list_major_student(sess: Session):
    """Prompt the user for the major, then list the students who have that major declared.
    :param sess:    The connection to the database.
    :return:        None
    """
    major: Major = select_major(sess)
    recs = sess.query(Major).join(StudentMajor, StudentMajor.majorName == Major.name).join(
        Student, StudentMajor.studentId == Student.studentID).filter(
        Major.name == major.name).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}")

def list_student_section(sess: Session):
    #Prompt user for student and list sections enrolled in that section
    student: Student = select_student(sess)
    students_in_section = sess.query(Student).join(Enrollment, Student.studentID == Enrollment.studentID).join(
        Section, Enrollment.sectionID == Section.sectionID).filter(Student.studentID == student.studentID).add_columns(
        Student.lastName, Student.firstName, Section.departmentAbbreviation, Section.courseNumber,
        Section.sectionNumber, Section.semester).all()
    for stu in students_in_section:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Department: {stu.departmentAbbreviation},"
              f"Course: {stu.courseNumber}, Section: {stu.sectionNumber}, Semester: {stu.semester}")

def list_section_student(sess: Session):
    #Prompt user for section and list the students enrolled in it
    section: Section = select_section(sess)
    sections_in_student = sess.query(Section).join(Enrollment, Enrollment.sectionID == Section.sectionID).join(
        Student, Enrollment.studentID == Student.studentID).filter(Student.studentID == section.sectionID).add_columns(
        Student.lastName, Student.firstName, Section.departmentAbbreviation, Section.courseNumber,
        Section.sectionNumber, Section.semester).all()
    for stu in sections_in_student:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Department: {stu.departmentAbbreviation},"
              f"Course: {stu.courseNumber}, Section: {stu.sectionNumber}, Semester: {stu.semester}")


def move_course_to_new_department(sess: Session):
    """
    Take an existing course and move it to an existing department.  The course has to
    have a department when the course is created, so this routine just moves it from
    one department to another.

    The change in department has to occur from the Course end of the association because
    the association is mandatory.  We cannot have the course not have any department for
    any time the way that we would if we moved it to a new department from the department
    end.

    Also, the change in department requires that we make sure that the course will not
    conflict with any existing courses in the new department by name or number.
    :param sess:    The connection to the database.
    :return:        None
    """
    print("Input the course to move to a new department.")
    course = select_course(sess)
    old_department = course.department
    print("Input the department to move that course to.")
    new_department = select_department(sess)
    if new_department == old_department:
        print("Error, you're not moving to a different department.")
    else:
        # check to be sure that we are not violating the {departmentAbbreviation, name} UK.
        name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == new_department.abbreviation,
                                                    Course.name == course.name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            # Make sure that moving the course will not violate the {departmentAbbreviation,
            # course number} uniqueness constraint.
            number_count = sess.query(Course). \
                filter(Course.departmentAbbreviation == new_department.abbreviation,
                       Course.courseNumber == course.courseNumber).count()
            if number_count != 0:
                print("We already have a course by that number in that department.  Try again.")
            else:
                course.set_department(new_department)


def select_student_from_list(session):
    """
    This is just a cute little use of the Menu object.  Basically, I create a
    menu on the fly from data selected from the database, and then use the
    menu_prompt method on Menu to display characteristic descriptive data, with
    an index printed out with each entry, and prompt the user until they select
    one of the Students.
    :param session:     The connection to the database.
    :return:            None
    """
    # query returns an iterator of Student objects, I want to put those into a list.  Technically,
    # that was not necessary, I could have just iterated through the query output directly.
    students: [Department] = list(sess.query(Department).order_by(Department.lastName, Department.firstName))
    options: [Option] = []  # The list of menu options that we're constructing.
    for student in students:
        # Each time we construct an Option instance, we put the full name of the student into
        # the "prompt" and then the student ID (albeit as a string) in as the "action".
        options.append(Option(student.lastName + ', ' + student.firstName, student.studentId))
    temp_menu = Menu('Student list', 'Select a student from this list', options)
    # text_studentId is the "action" corresponding to the student that the user selected.
    text_studentId: str = temp_menu.menu_prompt()
    # get that student by selecting based on the int version of the student id corresponding
    # to the student that the user selected.
    returned_student = sess.query(Department).filter(Department.studentId == int(text_studentId)).first()
    # this is really just to prove the point.  Ideally, we would return the student, but that
    # will present challenges in the exec call, so I didn't bother.
    print("Selected student: ", returned_student)


def list_department_courses(sess):
    department = select_department(sess)
    dept_courses: [Course] = department.get_courses()
    print("Course for department: " + str(department))
    for dept_course in dept_courses:
        print(dept_course)


def boilerplate(sess):
    """
    Add boilerplate data initially to jump start the testing.  Remember that there is no
    checking of this data, so only run this option once from the console, or you will
    get a uniqueness constraint violation from the database.
    :param sess:    The session that's open.
    :return:        None
    """
    department: Department = Department('CECS', 'Computer Engineering Computer Science', 'John Smith', 'ECS',
                                        500, 'The study of computers')
    major1: Major = Major(department, 'Computer Science', 'Fun with blinking lights')
    major2: Major = Major(department, 'Computer Engineering', 'Much closer to the silicon')
    student1: Student = Student('Brown', 'David', 'david.brown@gmail.com')
    student2: Student = Student('Brown', 'Mary', 'marydenni.brown@gmail.com')
    student3: Student = Student('Disposable', 'Bandit', 'disposable.bandit@gmail.com')
    student1.add_major(major1)
    student2.add_major(major1)
    student2.add_major(major2)
    sess.add(department)
    sess.add(major1)
    sess.add(major2)
    sess.add(student1)
    sess.add(student2)
    sess.add(student3)
    sess.flush()  # Force SQLAlchemy to update the database, although not commit


def session_rollback(sess):
    """
    Give the user a chance to roll back to the most recent commit point.
    :param sess:    The connection to the database.
    :return:        None
    """
    confirm_menu = Menu('main', 'Please select one of the following options:', [
        Option("Yes, I really want to roll back this session", "sess.rollback()"),
        Option("No, I hit this option by mistake", "pass")
    ])
    exec(confirm_menu.menu_prompt())


if __name__ == '__main__':
    print('Starting off')
    logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))

    # Prompt the user for whether they want to introspect the tables or create all over again.
    introspection_mode: int = IntrospectionFactory().introspection_type
    if introspection_mode == START_OVER:
        print("starting over")
        # create the SQLAlchemy structure that contains all the metadata, regardless of the introspection choice.
        metadata.drop_all(bind=engine)  # start with a clean slate while in development

        # Create whatever tables are called for by our "Entity" classes that we have imported.
        metadata.create_all(bind=engine)
    elif introspection_mode == REUSE_NO_INTROSPECTION:
        print("Assuming tables match class definitions")

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')
