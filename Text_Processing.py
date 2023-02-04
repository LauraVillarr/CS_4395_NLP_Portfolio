# Homework 1
# Laura Villarreal

import sys
import re
import pathlib
import pickle


# Person class - holds the data about a person found in our data.csv file
class Person:
    def __init__(self, last, first, mi, emp_id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.emp_id = emp_id
        self.phone = phone

    # displays the data in a specific Person object
    def display(self):
        print("Employee id: " + self.emp_id)
        print("\t" + self.first + " " + self.mi + " " + self.last)
        print("\t" + self.phone + "\n")


'''
Processes the data of each employee to be in the correct format

Args: 
    employee_data: a list of data for employees
    Note that the data must be divided by commas and contain the values
    last name, first name, middle initial, employee id, and phone number in that order
    
Returns:
    a dict of Person objects
    
Example:
    >>>process_data(['WILLIAMS,WITTY,W,S4454,555-877.4321])
    >>>{'SA4454': Person object - last = Williams, first = Witty, mi = W, emp_id = SA4454,
        phone = 555-877-4321}
'''


def process_data(employee_data):
    employee_dict = {}
    # each iteration corresponds to one employee
    for i in range(0, len(employee_data)):
        last, first, mi, emp_id, phone = employee_data[i].split(",")

        # modify first and last name to be in capital case
        first = first[0].upper() + first[1:].lower()
        last = last[0].upper() + last[1:].lower()

        # modify initial to be uppercase, if it exists
        if mi:
            mi = mi.upper()
        else:
            mi = 'X'

        # id is valid if it starts with 2 capital letters followed by 4 numbers
        valid_id = re.match("^[A-Z]{2}[0-9]{4}$", emp_id)
        # don't continue until the user enters a valid ID
        while not valid_id:
            print("ID invalid: " + emp_id)
            print("an ID must contain 2 capital letters followed by 4 numbers")
            emp_id = input("Please input the ID for employee " + first + " " + mi + " " + last + ": ")
            valid_id = re.match("^[A-Z]{2}[0-9]{4}$", emp_id)

        # if the phone number is divided in spaces, substitute the spaces with -
        # this is to reduce the number of inputs a user has to manually enter for phone number
        phone = re.sub("\s", "-", phone)

        # phone number is valid if it is in the form 999-999-9999
        valid_phone = re.match("^[0-9]{3}-[0-9]{3}-[0-9]{4}$", phone)
        while not valid_phone:
            print("Phone number " + phone + " is invalid")
            phone = input("Enter phone number in the form 123-456-7890: ")
            valid_phone = re.match("^[0-9]{3}-[0-9]{3}-[0-9]{4}$", phone)

        # adding our corrected employee into the employees dict
        person = Person(last, first, mi, emp_id, phone)
        employee_dict[person.emp_id] = person

    return employee_dict


# get the data from the csv file from an argument
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: Data not found. Add a parameter specifying where to find the data.")
        quit()
    else:
        filepath = sys.argv[1]
        with open(pathlib.Path.cwd().joinpath(filepath), 'r') as f:
            read_data = f.read().splitlines()

        # reformat the employee data from the file to be in the correct format
        employees = process_data(read_data[1:])

        # pickle employees
        pickle.dump(employees, open('employees.pickle', 'wb'))

        # read pickle in
        employees_in = pickle.load(open('employees.pickle', 'rb'))

        print("\n\nEmployee list:\n")
        for employee_id in employees_in.keys():
            employees_in[employee_id].display()

