import logging
from menu_definitions import menu_main, debug_select, department_select
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Student import Student
from Department import Department
from Option import Option
from Menu import Menu


def add_student(session: Session):
    """
    Prompt the user for the information for a new student and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_email: bool = False
    lastName: str = ''
    firstName: str = ''
    email: str = ''
    # Note that there is no physical way for us to duplicate the student_id since we are
    # using the Identity "type" for studentId and allowing PostgreSQL to handle that.
    # See more at: https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-identity-column/
    while not unique_name or not unique_email:
        lastName = input("Student last name--> ")
        firstName = input("Student first name--> ")
        email = input("Student e-mail address--> ")
        name_count: int = session.query(Student).filter(Student.lastName == lastName,
                                                        Student.firstName == firstName).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name.  Try again.")
        if unique_name:
            email_count = session.query(Student).filter(Student.eMail == email).count()
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that e-mail address.  Try again.")
    newStudent = Student(lastName, firstName, email)
    session.add(newStudent)


def select_student_id(sess: Session) -> Student:
    """
    Prompt the user for a specific student by the student ID.  Generally
    this is not a terribly useful approach, but I have it here for
    an example.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    ID: int = -1
    while not found:
        ID = int(input("Enter the student ID--> "))
        id_count: int = sess.query(Student).filter(Student.studentId == ID).count()
        found = id_count == 1
        if not found:
            print("No student with that ID.  Try again.")
    return_student: Student = sess.query(Student).filter(Student.studentId == ID).first()
    return return_student


def select_student_first_and_last_name(sess: Session) -> Student:
    """
    Select a student by the combination of the first and last name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    lastName: str = ''
    firstName: str = ''
    while not found:
        lastName = input("Student last name to delete--> ")
        firstName = input("Student first name to delete--> ")
        name_count: int = sess.query(Student).filter(Student.lastName == lastName,
                                                     Student.firstName == firstName).count()
        found = name_count == 1
        if not found:
            print("No student by that name.  Try again.")
    oldStudent = sess.query(Student).filter(Student.lastName == lastName,
                                            Student.firstName == firstName).first()
    return oldStudent


def select_student_email(sess: Session) -> Student:
    """
    Select a student by the e-mail address.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    email: str = ''
    while not found:
        email = input("Enter the student email address --> ")
        id_count: int = sess.query(Student).filter(Student.eMail == email).count()
        found = id_count == 1
        if not found:
            print("No student with that email address.  Try again.")
    return_student: Student = sess.query(Student).filter(Student.eMail == email).first()
    return return_student


def find_student(sess: Session) -> Student:
    """
    Prompt the user for attribute values to select a single student.
    :param sess:    The connection to the database.
    :return:        The instance of Student that the user selected.
                    Note: there is no provision for the user to simply "give up".
    """
    find_student_command = student_select.menu_prompt()
    match find_student_command:
        case "ID":
            old_student = select_student_id(sess)
        case "first/last name":
            old_student = select_student_first_and_last_name(sess)
        case "email":
            old_student = select_student_email(sess)
        case _:
            old_student = None
    return old_student


def delete_student(session: Session):
    """
    Prompt the user for a student by the last name and first name and delete that
    student.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a student")
    oldStudent = find_student(session)
    session.delete(oldStudent)


def list_students(session: Session):
    """
    List all of the students, sorted by the last name first, then the first name.
    :param session:
    :return:
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    students: [Student] = list(session.query(Student).order_by(Student.lastName, Student.firstName))
    for student in students:
        print(student)


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
    students: [Student] = list(sess.query(Student).order_by(Student.lastName, Student.firstName))
    options: [Option] = []                      # The list of menu options that we're constructing.
    for student in students:
        # Each time we construct an Option instance, we put the full name of the student into
        # the "prompt" and then the student ID (albeit as a string) in as the "action".
        options.append(Option(student.lastName + ', ' + student.firstName, student.studentId))
    temp_menu = Menu('Student list', 'Select a student from this list', options)
    # text_studentId is the "action" corresponding to the student that the user selected.
    text_studentId: str = temp_menu.menu_prompt()
    # get that student by selecting based on the int version of the student id corresponding
    # to the student that the user selected.
    returned_student = sess.query(Student).filter(Student.studentId == int(text_studentId)).first()
    # this is really just to prove the point.  Ideally, we would return the student, but that
    # will present challenges in the exec call, so I didn't bother.
    print("Selected student: ", returned_student)


def add_department(session: Session):
    """
    Prompt the user for the information for a new student and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    # unique constraints
    unique_name: bool = False  # name (primary key)
    unique_abbr: bool = False  # abbreviation
    unique_chair: bool = False  # chair name
    unique_office: bool = False # office
    unique_building: bool = False # building
    unique_desc: bool = False  # description

    # attributes
    name: str = ''
    abbreviation: str = ''
    chair_name: str = ''
    building: str = ''
    office: int = 0
    description: str = ''

    while not unique_name:
        name = input("Department name--> ")
        name_count: int = session.query(Department).filter(Department.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a department by that name.  Try again.")

    while not unique_abbr:
        abbreviation = input("Abbreviation--> ")
        abbr_count: int = session.query(Department).filter(Department.abbreviation == abbreviation).count()
        unique_abbr = abbr_count == 0
        if not unique_name:
            print("We already have a department by that abbreviation. Try again.")

    while not unique_chair:
        chair_name = input("Chair name--> ")
        chair_count: int = session.query(Department).filter(Department.chair_name == chair_name).count()
        unique_chair = chair_count == 0
        if not unique_chair:
            print("We already have a department with that chair. Try again.")

    while not unique_office:
        office = input("Office name--> ")
        office_count: int = session.query(Department).filter(Department.office == office).count()
        unique_office = office_count == 0
        if not unique_office:
            print("We already have a department in that office. Try again.")

    while not unique_building:
        building = input("Building name--> ")
        building_count: int = session.query(Department).filter(Department.building == building).count()
        unique_building = building_count == 0
        if not unique_building:
            print("We already have a department in that building. Try again.")


    while not unique_desc:
        description = input("Department description--> ")
        desc_count: int = session.query(Department).filter(Department.description == description).count()
        unique_desc = desc_count == 0
        if not unique_desc:
            print("We already have department by that description. Try again.")
        '''if unique_name:
            email_count = session.query(Student).filter(Student.eMail == email).count()
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that e-mail address.  Try again.")'''

    """
    abbreviation = input("Department Abbreviation--> ")
    chair_name = input("Department Chair Name--> ")
    building = input("Department Building--> ")
    office = input("Department Office--> ")
    """
    new_department = Department(name, abbreviation, chair_name, building, office, description)
    session.add(new_department)


def delete_department(session: Session):
    print("deleting department")
    oldDepartment = find_department(session)
    session.delete(oldDepartment)


def list_departments(session: Session):
    departments: [Department] = list(session.query(Department).order_by(Department.name))
    for d in departments:
        print(d)


def select_department_from_list(session):
    departments: [Department] = list(session.query(Department).order_by(Department.name))
    options: [Option] = []

    for d in departments:
        options.append(Option(d.abbreviation, d.name))

    tMenu = Menu('Department list', 'Select a department from this list', options)
    text_departmentId: str = tMenu.menu_prompt()
    returned_department = sess.query(Department).filter(Department.name == text_departmentId).first()
    print("Selected department: ", returned_department)


def find_department(sess: Session) -> Department:
    """
    Prompt the user for attribute values to select a single student.
    :param sess:    The connection to the database.
    :return:        The instance of Student that the user selected.
                    Note: there is no provision for the user to simply "give up".
    """
    find_department_command = department_select.menu_prompt()
    match find_department_command:
        case "name":
            old_department = select_department_name(sess)

        case "abbreviation":
            old_department = select_department_abbr(sess)

        case "chairName":
            old_department = select_department_chair_name(sess)

        case "building/office":
            old_department = select_department_bldg_office(sess)

        case "description":
            old_department = select_department_description(sess)
        case _:
            old_department = None
    return old_department


def select_department_name(sess: Session) -> Department:
    found: bool = False
    name: str = ''
    while not found:
        name = input("Enter the department name --> ")
        name_count: int = sess.query(Department).filter(Department.name == name).count()
        found = name_count == 1
        if not found:
            print("No department with that name.  Try again.")
    return_department: Department = sess.query(Department).filter(Department.name == name).first()
    return return_department


def select_department_abbr(sess):
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Enter the department abbreviation --> ")
        abbr_count: int = sess.query(Department).filter(Department.abbreviation == abbreviation).count()
        found = abbr_count == 1
        if not found:
            print("No department with that name.  Try again.")
    return_department: Department = sess.query(Department).filter(Department.abbreviation == abbreviation).first()
    return return_department


def select_department_chair_name(sess):
    found: bool = False
    chair: str = ''
    while not found:
        chair = input("Enter the department chair name --> ")
        chair_count: int = sess.query(Department).filter(Department.chair_name == chair).count()
        found = chair_count == 1
        if not found:
            print("No department with that chair name.  Try again.")
    return_department: Department = sess.query(Department).filter(Department.chair_name == chair).first()
    return return_department


def select_department_bldg_office(sess):
    found: bool = False
    building: str = ''
    office: int = -1
    while not found:
        building = input("Enter the department building --> ")
        office = int(input("Enter the department office number --> "))
        office_bldg_count: int = sess.query(Department).filter(Department.building == building,
                                                               Department.office == office).count()
        found = office_bldg_count == 1
        if not found:
            print("No department with that office and building.  Try again.")
    return_department: Department = sess.query(Department).filter(Department.building == building,
                                                                  Department.office == office).first()
    return return_department


def select_department_description(sess):
    found: bool = False
    description: str = ''
    while not found:
        description = input("Enter the department description --> ")
        desc_count: int = sess.query(Department).filter(Department.description == description).count()
        found = desc_count == 1
        if not found:
            print("No department with that description.  Try again.")
    return_department: Department = sess.query(Department).filter(Department.description == description).first()
    return return_department


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

    metadata.drop_all(bind=engine)  # start with a clean slate while in development

    # Create whatever tables are called for by our "Entity" classes.
    metadata.create_all(bind=engine)

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')
