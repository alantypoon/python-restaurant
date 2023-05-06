from operator import attrgetter

from Customers import *
from Order import *

class Restaurant():

    def __init__(self):

        # order = Order('dine-in', None)    # testing order

        self.customers = Customers()

        # testint customers
        self.customers.add_customer('John Chan', '1', '12/12/2000', '1', "Hong Kong")
        self.customers.add_customer('Tom Leung', '2', '11/11/2001', '2', "")
        
        # print(self.customers)
        self.start()

        
    def start(self):
        self.loggedin_customer = None

        while True:
            print("Please enter 1 for Sign up")
            print("Please enter 2 for Sign in")
            print("Please enter 3 for Quit.")            
            option = input("Please select an option (1, 2 or 3): ")
            if option == '1':
                self.customers.signup()
            elif option == '2':
                self.loggedin_customer = self.customers.signin()
                if self.loggedin_customer:
                    self.loggedin_menu()
            elif option == '3':
                break

        # clear the memory        
        if self.loggedin_customer:
            del self.loggedin_customer

        print("Thank You for using the Application.")

    ###

    def loggedin_menu(self):
        while True:
            print("Please Enter 2.1 to start Ordering. ")
            print("Please Enter 2.2 to Print Statistics. ")
            print("Please Enter 2.3 for Logout")
            option = input("Please select an option (2.1, 2.2 or 2.3): ")        
            if option == '2.1':
                self.__start_ordering()
                
            elif option == '2.2':
                self.__print_statistics()

            elif option == '2.3':  
                break

    
    ###

    def __start_ordering(self):

        while True:
            type = ''

            while True:
                print("Please Enter 1 for Dine in. ")
                print("Please Enter 2 for Order Online. ")
                print("Please Enter 3 to go to Login Page. ")
                option = input("Please select an option (1, 2 or 3): ")
                if option == '1':
                    type = 'dine-in'
                    break           
                elif option == '2':
                    type = self.__select_delivery_mode()
                    break           
                elif option == '3':
                    break
            
            if type:
                order = Order(type, self.loggedin_customer)
                if order.confirmed:
                    order.show_receipt()
                    self.loggedin_customer.add_order(order)
                    break
                # else:
                    # cancelled because of no home delivery address
                    # taken back to the Ordering Menu to select other option.
            else:
                # option = 3
                break

    ###            

    def __select_delivery_mode(self):
        type = ''
        while True:
            print("Enter 1 for Self Pickup. ")
            print("Enter 2 for Home Delivery. ")
            print("Enter 3 to go to Previous Menu. ")
            option = input("Please select an option (1, 2 or 3): ")
            if option == '1':
                type = 'pick-up'
                break
            elif option == '2':
                type = 'delivery'
                break
            elif option == '3':
                break
        return type

    ###

    def __print_statistics(self):

        while True:
            format = ''
            option = input("Please Enter the Option to Print the Statistics.\n"+
                "1 - All Dine in Orders.\n"+
                "2 - App Pick up Orders. \n"+
                "3 - All Deliveries. \n"+
                "4 - All Orders (Ascending Order). \n"+
                "5 - Total Amount Spent on All Orders. \n"+
                "6 - To go to Previous Menu. ")
            if option == "1":
                format = 'all-dine-in'
            elif option == "2":
                format = 'all-pick-up'
            elif option == "3":
                format = 'all-delivery'
            elif option == "4":
                format = 'all-order'
            elif option == "5":
                format = 'total-amount'
            elif option == "6":
                break

            self.__print_format(format)

###

    def __print_format(self, format):

        orders = self.loggedin_customer.orders

        if format == 'total-amount':

            # calculate total
            total = 0
            for order in orders:
                total += order.amount
            print(f"\nThe Total amount spent on all orders AUD: {total}\n")

        else:
        
            if format == 'all-order':
                orders = sorted(orders, key=attrgetter('order_id'), reverse=True)
            
            # print header
            print()
            line = "{:<13} {:<12} {:<23} {:<20}"
            self.__draw_line()
            print(line.format('Order ID', 'Date', 'Total Amount Paid' , 'Type of Order'))
            self.__draw_line()
            # print oders
            for order in orders:
                print_order = False
                if format == 'all-order':
                    print_order = True
                elif order.type == 'dine-in' and format == 'all-dine-in':
                    print_order = True
                elif order.type == 'pick-up' and format == 'all-pick-up':
                    print_order = True
                elif order.type == 'delivery' and format == 'all-delivery':
                    print_order = True
                if print_order:
                    print(line.format(order.order_id, order.order_date, order.amount, order.type))
            # finish line
            self.__draw_line()
            
    ###

    def __draw_line(self):
        print("-"*70)

