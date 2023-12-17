import pymongo
from pymongo import MongoClient
from pprint import pprint
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu


def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def select_student(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from
                    the database.
    """
    # Create a connection to the students collection from this database
    collection = db["students"]
    found: bool = False
    lastName: str = ''
    firstName: str = ''
    while not found:
        lastName = input("Student's last name--> ")
        firstName = input("Student's first name--> ")
        name_count: int = collection.count_documents({"last_name": lastName, "first_name": firstName})
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    found_student = collection.find_one({"last_name": lastName, "first_name": firstName})
    return found_student


def select_department(db):
    collection = db["department"]
    found: bool = False
    name: str = ''
    while not found:
        name = input("Department's name--> ")
        name_count: int = collection.count_documents({"name": name})
        found = name_count == 1
        if not found:
            print("No department found by that name. Try again.")
    found_department = collection.find_one({"name": name})
    return found_department


def add_department(db):
    # collection pointer to department collections in db
    collection = db["department"]

    unique_name: bool = False
    unique_abbreviation: bool = False
    unique_chair_name: bool = False
    unique_building_and_office: bool = False
    unique_description: bool = False

    name: str = ''
    abbreviation: str = ''
    chair_name: str = ''
    building: str = ''
    office: int = 0
    description: str = ''

    while not unique_abbreviation or not unique_name or not unique_chair_name or not unique_building_and_office or not unique_description:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        chair_name = input("Department chair name--> ")
        building = input("Department building--> ")
        office = int(input("Department office--> "))
        description = input("Department description--> ")

        name_count: int = collection.count_documents({"name": name})
        unique_name = name_count == 0
        if not unique_name:
            print("There is already a department with that name. Try again")

        if unique_name:
            abbreviation_count = collection.count_documents({"abbreviation": abbreviation})
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print("We already have a department with that abbreviation.  Try again.")
            if unique_abbreviation:
                chair_count = collection.count_documents({"chair_name": chair_name})
                unique_chair_name = chair_count == 0
                if not unique_chair_name:
                    print("We already have a department with that chair name. Try again.")
                if unique_chair_name:
                    build_office_count = collection.count_documents({"building": building, "office": office})
                    unique_building_and_office = build_office_count == 0
                    if not unique_building_and_office:
                        print("We already have a department with that building and office. Try again.")
                    if unique_building_and_office:
                        description_count = collection.count_documents({"description": description})
                        unique_description = description_count == 0
                        if not unique_description:
                            print("We already have a department with that description. Try again.")
    department = {
        "name": name,
        "abbreviation": abbreviation,
        "chair_name": chair_name,
        "building": building,
        "office": office,
        "description": description
    }
    result = collection.insert_one(department)


def list_department(db):
    departments = db["department"].find({}).sort([("name", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for department in departments:
        pprint(department)


def delete_department(db):

    department = select_department(db)
    # Create a "pointer" to the students collection within the db database.
    departments = db["department"]
        # student["_id"] returns the _id value from the selected student document.
    deleted = departments.delete_one({"_id": department["_id"]})
        # The deleted variable is a document that tells us, among other things, how
        # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} departments.")


if __name__ == '__main__':
    password: str = 'Janeaddams1' #getpass.getpass('Mongo DB password -->')
    username: str = "CECS-323-Fall-2023-user" #input('Database username [CECS-323-Spring-2023-user] -->') or \
                    #"CECS-323-Spring-2023-user"
    project: str = "CECS-323-Fall-2023" #input('Mongo project name [cecs-323-spring-2023] -->') or \
                   #"CECS-323-Spring-2023"
    hash_name: str = "puxnikb" #input('7-character database hash [puxnikb] -->') or "puxnikb"
    cluster = 'mongodb+srv://omeedenshaie01:Janeaddams1@cluster0.i9ivbqp.mongodb.net/?retryWrites=true&w=majority'
    print(f"Cluster: mongodb+srv://{username}:********@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient(cluster)
    db = client["SingleCollection"]
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.

    # Print off the collections that we have available to us, again more of a test than anything
    # db will be the way that we refer to the database from here on out.

    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())
    # student is our students collection within this database.
    # Merely referencing this collection will create it, although it won't show up in Atlas until
    # we insert our first document into this collection.
    departments = db["department"]

    dep_count = departments.count_documents({})
    print(f"Departments in the collection so far: {dep_count}")

    # ************************** Set up the students collection
    departments_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': "object",
                'description': "departments_table",
                'required': ["name", "abbreviation", "chair_name", "building", "office", "description"],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'name': {
                        'bsonType': "string",
                        'minLength': 10,
                        'maxlength': 50,
                        'description': "the name of the department"
                    },
                    'abbreviation': {
                        'bsonType': "string",
                        'minLength': 1,
                        'maxlength': 6,
                        'description': "the abbreviation for the department",
                    },
                    'chair_name': {
                        'bsonType': "string",
                        'minLength': 1,
                        'maxLength': 80,
                        'description': "the person who is in charge of the department",
                    },
                    'building': {
                        'enum': ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],
                        'bsonType': "string",
                        'description': "the building of the department",
                    },
                    'office': {
                        'bsonType': "integer",
                        'description': "office number",
                    },
                    'description': {
                        'bsonType': "string",
                        'minLength': 10,
                        'maxlength': 80,
                        'description': "description of building"
                    }
                }
            }
        }
    }

    dep_indexes = departments.index_information()
    if 'department_name' in dep_indexes.keys():
        print("name is present.")
    else:
        # Create a single UNIQUE index on names.
        departments.create_index([('name', pymongo.ASCENDING)], name="department_names")

    if 'department_abbreviation' in dep_indexes.keys():
        print("department_abbreviation index present.")
    else:
        # Create a UNIQUE index on just the abbreviation address
        departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name='department_abbreviation')

    if 'department_chair_name' in dep_indexes.keys():
        print("chair_name is present")
    else:
        departments.create_index([("chair_name", pymongo.ASCENDING)], unique=True, name='department_chair_name')

    if 'department_building' in dep_indexes.keys():
        print("building is present")
    else:
        departments.create_index([("building", pymongo.ASCENDING)], unique=False, name='department_building')

    if 'department_office' in dep_indexes.keys():
        print("office is present")
    else:
        departments.create_index([("office", pymongo.ASCENDING)], unique=False, name='department_office')

    if 'department_description' in dep_indexes.keys():
        print("description is present")
    else:
        departments.create_index([("description", pymongo.ASCENDING)], unique=True, name='department_description')

    db.departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)], unique=True)

    pprint(departments.index_information())
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)

