# -------------------------------------------------------------------------- #
# Title: Assignment06
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   GCarter,11/18/2026,Added FileProcessor and IO classes using
#   separation of concerns
# --------------------------------------------------------------------------- #
import json

# Define the Data Constants
MENU: str = """
---- Course Registration Program ----
Select from the following menu:
1. Register a student for a course
2. Show current data
3. Save data to a file
4. Exit the program
-------------------------------------
"""
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
menu_choice: str = '' # string set to empty
students: list = []  # table of student data (list of dictionary rows)


# Processing --------------------------------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with JSON files.

    ChangeLog: (Who, When, What)
    GCarter,11/18/2026,Created class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        Reads data from a JSON file into a list of dictionary rows.

        ChangeLog: (Who, When, What)
        GCarter,11/18/2026,Created function

        :return: list of dictionary rows
        """
        file = None
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages("The file must exist before "
                                     "running this script!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error "
                                     "reading the file!", e)
        finally:
            if file is not None and file.closed == False:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        Writes a list of dictionary rows to JSON file, then shows what was saved.

        ChangeLog: (Who, When, What)
        GCarter,11/18/2026,Created function

        :return: None
        """
        file = None
        try:
            file = open(file_name, "w")
            json.dump(student_data, file, indent=2)
            file.close()
            print("The following data was saved to file!")
            IO.output_student_courses(student_data=student_data)
        except TypeError as e:
            IO.output_error_messages("Please check that the data is a valid "
                                     "JSON format.", e)
        except Exception as e:
            IO.output_error_messages("There was a problem writing to "
                                     "the file. "
                                     "Please check that the file is not open by "
                                     "another program.", e)
        finally:
            if file is not None and file.closed == False:
                file.close()


# Presentation ------------------------------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input
    and output.

    ChangeLog: (Who, When, What)
    GCarter,11/18/2026,Created class
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        Displays a custom error message, plus technical details when an exception
        is passed in.

        ChangeLog: (Who, When, What)
        GCarter,11/18/2026,Created function

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """
        Displays the menu of choices to the user.

        ChangeLog: (Who, When, What)
        GCarter,11/18/2026,Created function

        :return: None
        """
        print()
        print(menu)
        print()

    @staticmethod
    def input_menu_choice():
        """
        Gets a menu choice from the user and checks that it is 1, 2, 3, or 4.

        ChangeLog: (Who, When, What)
        GCarter,11/18/2026,Created function

        :return: string with the user's choice
        """
        choice = "0"
        try:
            choice = input("What would you like to do: ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())
        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """
        Displays each student row as comma-separated values.

        ChangeLog: (Who, When, What)
        GCarter,11/18/2026,Created function

        :return: None
        """
        print("-" * 50)
        for student in student_data:
            print(f'{student["FirstName"]},{student["LastName"]},'
                  f'{student["CourseName"]}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """
        Gets a student's first name, last name, and course name from the user,
        then adds them to the list of dictionary rows.

        ChangeLog: (Who, When, What)
        GCarter,11/18/2026,Created function

        :return: list of dictionary rows
        """
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should only contain letters.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should only contain letters.")
            course_name = input("Please enter the name of the course: ")
            student = {"FirstName": student_first_name,
                       "LastName": student_last_name,
                       "CourseName": course_name}
            student_data.append(student)
            print(f"You have registered {student_first_name} {student_last_name} "
                  f"for {course_name}.")
        except ValueError as e:
            IO.output_error_messages("That value is not the correct type "
                                     "of data!", e)
        except Exception as e:
            IO.output_error_messages("There was a problem with your entered "
                                     "data.", e)
        return student_data


# Main body of the script -------------------------------------------------- #

# When the program starts, read the file data into a list of dictionary rows
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and process the data
while True:

    # Present the menu of choices
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":  # Register a student
        students = IO.input_student_data(student_data=students)
        continue

    elif menu_choice == "2":  # Show current data
        IO.output_student_courses(student_data=students)
        continue

    elif menu_choice == "3":  # Save data to a file
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    elif menu_choice == "4":  # Stop the loop
        break

print("Program Ended")