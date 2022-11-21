import csv
from datetime import date, datetime
import datetime
import time
import re
list1 = []
all_cars = []
customer = []
cust_email = {}
rented_car_dict = {}
def print_head():
    '''
    Print heading of menu
    '''
    print('*'*75)
    print()
    print('hello !!! this is rent car app'.upper())
    print()
    print('*'*75)

def all_cars_list():
    all_cars.clear()
    with open("Vehicles.txt", "r", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            all_cars.append(row[0])
    file.close()

def customer_list():
    customer.clear()
    cust_email.clear()
    with open("Customers.txt", "r", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            customer.append(row[3])
            cust_email[row[3]] = row[1]
    file.close()

def rent_car():
    # Ask for car registration Number
    ID = input('Select the car number you want to rent: ')
    # Initialize the all_cars_list inorder to insert all available cars reg number to a list this will be used to check if car exists
    # similar to the rented_cars_list which will be used to check if the car is rented or not
    all_cars_list()
    rented_cars_list()
    if ID not in all_cars:
        print("A car with that Registration Number does not exsits")
    elif ID in list1:
        print("The Car is Not available")
    else:
        # if car is available
        date1 = input('ENter date of birth  (dd/mm/yyyy): ')
        # raise an exception if the date input by user is invalid
        try:
            # check date formart if it is in %d/%m/%Y' formart
            valid_date = time.strptime(date1, '%d/%m/%Y')
            vf = valid_date.tm_year
            # calculate the user date by using the date input by user
            age = calculate_age(vf)
            # check if user is above 100 years or below 18 years
            if age > 100   :
                print("Over Age")
            elif age < 18 :
                print ("Under Age")
            else:
                # if user has the required date then proceed
                customer_list()
                # get user name to check if he/she exists in the Customers.txt
                customer_detail = input("Enter Your Email: ")
                if customer_detail in customer:
                    # if customer Exists return the name of user and car rented then append the car rented to the rentedVehicles.txt
                    print(f"Hello {customer_detail}")
                    print(f"You rented the car {ID}")
                    # append car to rentedVehicles.txt
                    log = open("rentedVehicles.txt", 'a')
                    today_dt = datetime.datetime.now()
                    d1 = today_dt.strftime("%d/%m/%Y %H:%M")
                    log.write(f"{ID},{date1},{d1}\n")
                    log.close()
                else:
                    email_pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"  
                    # if customer dosent exits create a new one append the customer to the customers.txt file
                    name = input("Please Enter Your first name: ")
                    last_name = input("Please Enter Your last name: ")
                    email = input("Please Enter Your Email name: ")
                    pattern = re.compile(email_pattern)
                    if not re.match(pattern, email):
                        print(f"{email} email is invalid")
                    else:
                        # append new customer to file
                        cust_file = open("Customers.txt", 'a')
                        now = datetime.datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M")
                        print(dt_string)
                        cust_file.write(f"{dt_string},{name},{last_name},{email}\n")
                        # append the rented vehicle to the rentedVehicles.txt file
                        log = open("rentedVehicles.txt", 'a')
                        log.write(f"{ID},{date1},{dt_string}\n")
                        log.close()
                        print(f"Hello {name}")
                        print(f"You rented the car {ID}")
                        cust_file.close()
        except ValueError:
            print('Invalid date!')

def count_money():
    money_list = []
    with open("transActions.txt", "r", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            money_list.append(float(row[5]))
    total_money = sum(money_list)
    print(f"The total amount of money is {total_money} euros")

def return_car():
    ID = input("Enter register plate number of the car to be returned.")
    all_cars_list()
    rented_cars_list()
    if ID not in all_cars:
        print("A car with that Registration Number does not exsits")
    elif ID not in list1:
        print("The Car is Not Rented")
    else:
        veh = {}
        with open("Vehicles.txt", "r", newline="") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                veh[row[0]] = row[2]
        file.close()
        with open("rentedVehicles.txt", "r", newline="") as rent:
            rented_veh = {}
            eader = csv.reader(rent, delimiter=",")
            for row1 in eader:
                rented_veh[row1[0]] = row1[2]
        rent.close()
        daily_price = int(veh[ID])
        td = datetime.date.today()
        td.strftime("%d/%m/%Y")
        s1 = str(rented_veh[ID]).split()
        dys = datetime.datetime.strptime(s1[0], "%d/%m/%Y").date()
        num_days = td - dys
        print(abs(num_days.days))
        results = float(daily_price * num_days.days)
        round(results, 2)
        customer_list()
        client_info = input("Enter email")

        log = open("transActions.txt", 'a')
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M")
        log.write(f"{ID},{cust_email[client_info]},{rented_car_dict[ID]},{dt_string},{num_days.days},{results}\n")
        log.close()
        remove_car_rented_vehicles("rentedVehicles.txt", ID)
        


def remove_car_rented_vehicles(file, ID):
    with open(file, "r+", newline="") as rent:
        new_file = rent.readlines()
        rent.seek(0)
        for line in new_file:
            if ID not in line:
                rent.write(line)
        rent.truncate()
    rent.close() 

def calculate_age(birthdate):
    # Get the current date
    today = datetime.date.today()
    return today.year - birthdate


    
def rented_cars_list():
    list1.clear()
    rented_car_dict.clear()

    with open("rentedVehicles.txt", "r", newline="") as rent:
        
        eader = csv.reader(rent, delimiter=",")
        for row1 in eader:
            list1.append(row1[0])
            rented_car_dict[row1[0]] = row1[2]
    rent.close()


def available_cars():
    rented_cars_list()

    with open("Vehicles.txt", "r", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        
        for row in reader:
            if row[0] not in list1:
                try:
                    print(f"* Reg. nr:{row[0]}, Model: {row[1]}, Price per day:{row[2]}, Properties:{row[3]} ,{row[4]}")
                except Exception:
                    print(f"* Reg. nr:{row[0]}, Model: {row[1]}, Price per day:{row[2]}, Properties:{row[3]}")

def print_menu(menu):
    '''
    Print menu items
    '''
    print()
    for item in menu:
        print(item, end='   ')
    print()
    print()
    print('*'*75)


def main():
    print_head()

    while True:
        print("You may select one of the following:\n")
        menu = ['   1 - List available cars\n', '2 - Rent a car\n',
                '3 - Return a car\n', '4 - Count the money\n', '0 - Exit']
        print_menu(menu)
        choice = input('What is your selection? '.upper())
        print()

        # SHOW ALL
        if choice == '1':
            print('The following cars are available:'.upper())
            available_cars()
            print()
        elif choice == "2":
            rent_car()
        elif choice == "3":
            return_car()
        elif choice == "4":
            count_money()

        # QUIT
        elif choice == '0':
            print('Thanks for using rent car app. Bye.'.upper())
            break
            print()

        # WRONG CHOICE
        else:
            print('your choice is unknown'.upper())
            print()


main()