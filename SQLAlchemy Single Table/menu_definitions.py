from Menu import Menu
from Option import Option
"""
This little file just has the menus declared.  Each variable (e.g. menu_main) has 
its own set of options and actions.  Although, you'll see that the "action" could
be something other than an operation to perform.

Doing the menu declarations here seemed like a cleaner way to define them.  When
this is imported in main.py, these assignment statements are executed and the 
variables are constructed.  To be honest, I'm not sure whether these are global
variables or not in Python.
"""

# The main options for operating on Students.
menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add student", "add_student(sess)"),
    Option("Delete student", "delete_student(sess)"),
    Option("List all students", "list_students(sess)"),
    Option("Select student from list", "select_student_from_list(sess)"),
    Option("Add department", "add_department(sess)"),
    Option("List all departments", "list_departments(sess)"),
    Option("Select department from list", "select_department_from_list(sess)"),
    Option("Delete departments", "delete_department(sess)"),
    Option("Exit", "pass")
])

# A menu for how the user will specify which student they want to access,
# given that there are three separate candidate keys for Student.
student_select = Menu('student select', 'Please select how you want to select a student:', [
    Option("ID", "ID"),
    Option("First and last name", "first/last name"),
    Option("Electronic mail", "email")
])


department_select = Menu('department select', 'Please select how you want to select a department:', [    
    Option("Name", "Name"),    
    Option("Abbreviation", "Abbreviation"),    
    Option("Chair name", "Chain name"),    
    Option("Office", "Office"),   
    Option("Building", "Building"),    
    Option("Description", "Description")
])

# A menu to prompt for the amount of logging information to go to the console.
debug_select = Menu('debug select', 'Please select a debug level:', [
    Option("Informational", "logging.INFO"),
    Option("Debug", "logging.DEBUG"),
    Option("Error", "logging.ERROR")
])
