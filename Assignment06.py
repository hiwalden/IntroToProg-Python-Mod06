# ------------------------------------------------------------------------------------------ #
# Title: Assignment06_Starter
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   WMarcus, 3/2/25, Created Script
# ------------------------------------------------------------------------------------------ #

#PACKAGES -------
import json

# CONSTANTS -----
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# VARIABLES --------
menu_choice: str  # Hold the choice made by the user.
students: list = []  # a table of student data

#PRESENTATION --------
class IO:
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        This function displays a technical error message if an exception is raised.
        Change Log:
        WMarcus, 3/2/25, Created Function
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu:str):
        """
        This function prints the MENU constant.
        Change Log:
        WMarcus, 3/2/25, Created Function
        """
        global MENU
        print(MENU)

    @staticmethod
    def input_menu_choice():
        """
        This function receives the user's choice from MENU, and addresses invalid choices.
        return: string with user choice
        Change Log:
        WMarcus, 3/2/25, Created Function
        """
        global menu_choice
        try:
            menu_choice = input("Enter your menu choice number: ")
            if menu_choice not in ("1", "2", "3", "4"):
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())

        return menu_choice

    @staticmethod
    def output_student_courses(student_data:list):
        """
        This function displays all the student data, whether saved to file or awaiting writing to file.
        Change Log:
        WMarcus, 3/2/25, Created Function
        """
        global students
        print("-" * 50)
        for student in students:
            print(f'Student {student["FirstName"]} '
                f'{student["LastName"]} is enrolled in {student["CourseName"]}')
            print("-" * 50)

    @staticmethod
    def input_student_data(student_data:list):
        """
        This function requests and receives user input about student registration.
        return: A nested list containing user input
        Change Log:
        WMarcus, 3/2/25, Created Function
        """
        student_first_name: str = ''  # Holds the first name of a student entered by the user.
        student_last_name: str = ''  # Holds the last name of a student entered by the user.
        course_name: str = ''  # Holds the name of a course entered by the user.
        student_data: dict = {}  # one row of student data
        global students
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("No student name may contain numbers or characters")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("No student name may contain numbers or characters.")
            course_name = input("Please enter the name of the course: ")
            student_data = {"FirstName": student_first_name,
                            "LastName": student_last_name,
                            "CourseName": course_name}
            students.append(student_data)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages("Please re-attempt information entry.", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        return students

#DATA STORAGE -------
class FileProcessor:
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        This function reads data from the JSON file into a list of dictionary rows.
        return: A list of dictionaries
        Change Log:
        WMarcus, 3/2/25, Created Function
        """
        try:
            file = open(FILE_NAME, "r")
            student_data = json.load(file)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages("Text file must exist before running this script!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        finally:
            if file.closed == False:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name:str, student_data:list):
        """
        This function writes a list of dictionaries to a JSON, then prints the data that was written.
        Change Log:
        WMarcus, 3/2/25, Created Function
        """
        json_data: str = ''  # Holds combined string data in a json format.
        file = None  # Holds a reference to an opened file.
        global students
        try:
            file = open(FILE_NAME, "w")
            json.dump(students, file)

            file.close()
            print("The following data was saved to file!")
            for student in students:
                print(f'Student {student["FirstName"]} {student["LastName"]} is enrolled in {student["CourseName"]}')
        except FileNotFoundError as e:
                IO.output_error_messages("Text file must exist before running this script!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        finally:
            if file.closed == False:
                file.close()

#LOGIC---------
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)
while True:
    IO.output_menu(menu = MENU)
    IO.input_menu_choice()
            # Input user data
    if menu_choice == "1":
        IO.input_student_data(student_data = students)
        continue
            # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(student_data = students)
        continue
            # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name = FILE_NAME, student_data = students)
        continue
            # Stop the loop
    elif menu_choice == "4":
            break

print("Program Ended")
