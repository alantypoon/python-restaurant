
import datetime
import re


class Customer():

    def __init__(self, name, mobile, dob, password, address):
        self.Name = name
        self.Mobile = mobile
        self.dob = dob
        self.password = password
        self.address = address
        self.orders = []

    ###

    def add_order(self, order):
        self.orders.append(order)

    ###

    def enter_address(self):
        while True:
            option = input ("Please enter your address: ")
            if option != '':
                self.address = option
                break
        return self.address

    ###

    def __str__(self):
        s = f"{self.Name}\t{self.Mobile}\t{self.dob}\t{self.password}\t{self.address}"
        for order in self.orders:
            s += str(self.orders)
        return s

class Customers():

    ###
    def __init__(self):
        self.customer_hash = {}
    
    ###

    def signup(self):
        while True:
            name = input("Please enter your name: ")
            address = input("Please enter your address or press enter to skip. ")
            mobile_number = input("Please enter your mobile number: ")
            dob_str = input("Please enter your date of birth in DD/MM/YYYY format with no space: ")
            password = input("Please enter your password: ")
            password_confirmation = input("Please enter your password: ")
            invalid_input = False  # flag to indicate if any input is invalid

            # validate mobile number
            if not self.__validate_mobile_number(mobile_number):
                print("You have entered an invalid mobile number. Please enter a valid 10-digit number starting with 0. Please start again:")
                invalid_input = True
    
            # validate date of birth
            try:
                dob = datetime.datetime.strptime(dob_str, '%d/%m/%Y')
            except:
                print("You have entered the date of birth in invalid format. Please enter in DD/MM/YYYY format. Please start again: ")
                invalid_input = True
            else:
                dob = datetime.datetime.strptime(dob_str, '%d/%m/%Y')
                age = datetime.datetime.now().year - dob.year
                if age < 21:
                    print("You are under 21 and cannot register.")
                    invalid_input = True
    
            # validate password
            if not self.__validate_password(password):
                print("You have entered an invalid password. Password must initiate with alphabets followed by either one of @, & and ending with numeric. Please start again: ")
                invalid_input = True
    
            # validate password confirmation
            if password != password_confirmation:
                print("Your passwords are not matching. Please start again.")
                invalid_input = True
    
            if invalid_input:
                # at least one input is invalid, continue loop
                continue
    
            self.add_customer(name, mobile_number, dob, password, address)
            print("You have successfully signed up.")

    ###            

    def signin(self):
        tries = 0
        while True:
            mobile = input("Please enter your username (mobile number): ")
            password = input("Please enter your password: ")
            user = self.__find(mobile, password)
            if user:
                print("You have successfully signed in.")
                print("Welcome " + user.Name)
                break
            else:
                print("This user is not found or the password is incorrect")                
        return user


    ###
    def add_customer(self, name, mobile, dob, password, address):
        if mobile in self.customer_hash:
            print("This mobile already exists")
        else: 
            self.customer_hash[mobile] = Customer(name, mobile, dob, password, address)
            

    ###
    def __find(self, mobile, password):
        if self.customer_hash[mobile]:
            return self.customer_hash[mobile]
        else:
            return 0
    ###

    def __validate_mobile_number(self, mobile_number):
        if len(mobile_number) == 10 and mobile_number[0] == '0' and mobile_number.isdigit():
            return True
        else:
            return False
    ###

    def __validate_password(self, password):
        format = "^[a-zA-Z]+[@&]+[0-9]+$"
        if re.search(format, password):
            return True
        else:
            return False
        
    ###
    def __str__(self):
        s = ''
        for mobile in self.customer_hash:
            s += str(self.customer_hash[mobile]) + "\n"            
        return s
