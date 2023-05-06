import datetime

from Item import *

class Order:

    # CONSTANTS
    FOOD_ITEMS = [
        Item(1, "Noodles", 2),
        Item(2, "Sandwich", 4),
        Item(3, "Dumpling", 6),
        Item(4, "Muffins", 8),
        Item(5, "Pasta", 10),
        Item(6, "Pizza", 20)
    ]
    DRINK_ITEMS = [
        Item(1, "Coffee", 2),
        Item(2, "Colddrink", 4),
        Item(3, "Shake", 6)
    ]

    # GLOBAL VAIRABLE
    unique_order_id = 0

    # CONSTRUCTOR 
    def __init__(self, type, customer):

        self.type = type
        self.customer = customer
        self.order_id = ''
        self.order_date = ''
        self.items_subtotal = 0
        self.service_charge = 0
        self.delivery_charge = 0
        self.amount = 0
        self.selected_items = []
        self.confirmed = False
        
        # order as many as items here
        self.__select_items()

        # confirm or cancel
        if self.__confirm_order():

            if self.type == 'delivery':

                if self.customer.address == '':
                    self.__enter_delivery_address()

                # no address menas canceling the order
                if self.customer.address == '':
                    # taken back to the Ordering Menu to select other option
                    self.confirmed = False
                else:
                    self.__input_delivery_details()
                    if self.distance_of_delivery > 15:
                        print(
                            "The distance from the restaurant is more than the applicable limits. " +
                            "You are provided with the option to Pick up the Order instead")
                        self.type = "pick-up"
                        self.__input_pickup_details()
                
            elif self.type == 'dine-in':
                self.__input_dinein_details()

            elif self.type == 'pick-up':
                self.__input_pickup_details()

            # double check if it is not cancelled
            if self.confirmed:
                self.__calculate_amount()
                Order.unique_order_id += 1
                self.order_id = "S" + str(Order.unique_order_id).zfill(3)
                self.order_date = datetime.datetime.now().strftime("%d/%m/%Y")
                # self.__show_receipt()

    ###
        
    def __enter_delivery_address(self):
        while True:
            option = input("You have not mentioned your address, while signing up. \n" + 
                "Please Enter Y if would like to enter your address.\n" +
                "Enter N if you would like to select other mode of order. "
            )
            if option == "Y":
                if self.customer.enter_address():
                    break
            elif option == "N":
                break
        
            
    # select items

    def __select_items(self):
        self.selected_items = []

        # select food items
        while True:
            item = self.__select_one_item(self.FOOD_ITEMS)
            if item:
                self.selected_items.append(item)
                self.__show_shopping_cart()
            else:
                break

        # select drink items
        if self.type == 'dine-in':
            while True:
                item = self.__select_one_item(self.DRINK_ITEMS)
                if item:
                    self.selected_items.append(item)
                    self.__show_shopping_cart()
                else:
                    break

    # input one item
    def __select_one_item(self, items):
        selected_item = 0
        while True:
            for item in items:
                print(f"Enter {item}")

            exit_id = item.id + 1
            if self.type == 'dine-in' and items == self.FOOD_ITEMS:
                option = input(f"Enter {exit_id} for Drinks Menu:")
            else:
                option = input(f"Enter {exit_id} for Checkout:")

            if option.isdigit():
                option = int(option)
            # selection
            if option == exit_id:
                break
            else:
                for item in items:
                    if item.id == option:
                        selected_item = item
                        break
                if selected_item:
                    break

        return selected_item
        
    ###

    def __confirm_order(self):

        self.__show_shopping_cart()

        while True:
            option = input('Please Enter Y to proceed to Checkout or \nEnter N to cancel the order:')
            if option == 'Y':
                self.confirmed = True
                break
            elif option == 'N':
                break

        return self.confirmed

    ###

    def __input_dinein_details(self):
        while True:
            option = input("Please enter the Date of Booking for Dine in (DD/MM/YYYY): ")
            if self.__validate_date(option):
                self.date_of_visit = option
                break

        while True:
            option = input("Please enter the Time of Booking for Dine in (HH:MM): ")
            if self.__validate_time(option):
                self.time_of_visit = option
                break            

        while True:
            option = input("Please enter the Number of Person: ")
            if self.__validate_distance(option):
                self.num_persons = int(option)
                break
        print('Thank You for entering the details, Your Booking is confirmed.')

    ###

    def __input_pickup_details(self):
        while True:
            option = input("Please enter the Date of Pick up (DD/MM/YYYY): ")
            if self.__validate_date(option):
                self.date_of_pickup = option
                break

        while True:
            option = input("Please enter the Time of Pick up (HH:MM): ")
            if self.__validate_time(option):
                self.time_of_pickup = option
                break            

        while True:
            option = input("Please enter the Name of the Persons: ")
            if option != '':
                self.name_of_pickup_persons = option
                break

        print('Thank You for entering the details, Your Booking is confirmed.')

    ###

    def __input_delivery_details(self):
        while True:
            option = input("Please enter the Date of Delivery (DD/MM/YYYY): ")
            if self.__validate_date(option):
                self.date_of_delivery = option
                break

        while True:
            option = input("Please enter the Time of Delivery (HH:MM): ")
            if self.__validate_time(option):
                self.time_of_delivery = option
                break            

        while True:
            option = input("Please enter the Distance from the restaurant (in KM): ")
            if self.__validate_distance(option):
                self.distance_of_delivery = int(option)
                break

        print('Thank you for your order, Your Order has been confirmed.')

    ###

    def __validate_date(self, date):
        try:
            if date != datetime.datetime.strptime(date, "%d/%m/%Y").strftime('%d/%m/%Y'):
                raise ValueError
            return True
        except ValueError:
            return False        

    ###

    def __validate_time(self, time):
        try:
            if time != datetime.datetime.strptime(time, "%H:%M").strftime('%H:%M'):
                raise ValueError
            return True
        except ValueError:
            return False        

    ###

    def __validate_distance(self, distance):
        if distance.isnumeric():
            return True
        else:
            return False

###
        
    def __calculate_amount(self):        
        self.items_subtotal = 0
        self.amount = 0
        self.service_charge = 0
        self.delivery_charge = 0

        for item in self.selected_items:
            self.items_subtotal += item.price

        if self.type == 'dine-in':
            self.service_charge = round(self.items_subtotal * 0.15, 2)

        elif self.type == 'delivery': 
            
            if self.distance_of_delivery < 5:
                self.delivery_charge = 5
            elif self.distance_of_delivery < 10:
                self.delivery_charge = 10
            elif self.distance_of_delivery < 15:
                self.delivery_charge = 18
            elif self.distance_of_delivery > 15:
                self.delivery_charge = 0

        self.amount = self.items_subtotal + self.service_charge + self.delivery_charge

        print(f'Your total payable amount is: {self.amount}', end = '')
        if self.service_charge > 0:
            print(f" inclusing AUD {self.service_charge} for Service Charges")
        elif self.delivery_charge > 0:
            print(' and there will be an additional charge for Delivery')
        else:
            print('')

    ###

    def __draw_line(self):
        print("\t" + "-"*50)
    
    ###    

    def __show_shopping_cart(self):            
        print(f"\tShopping Cart")
        self.__draw_line()
        for item in self.selected_items:
            print(f"\t{item}")
        self.__draw_line()

    ###

    def show_receipt(self):
        self.__draw_line()
        print(f"\tReceipt")
        self.__draw_line()
        print(f"\tOrder: {self.order_id}")
        print(f"\tDate: {self.order_date}")
        print(f"\tType: {self.type}")

        self.__draw_line()        
        for item in self.selected_items:
            print(f"\t{item}")
        self.__draw_line()

        print(f"\tSubtotal: {self.items_subtotal}")

        if self.service_charge:
            print(f"\tService charge: {self.service_charge}")

        if self.delivery_charge:
            print(f"\tDelivery charge: {self.delivery_charge}")

        print(f"\t>>> Total amount needed to be paid: AUD {self.amount}\n")

    ###

    def __str__(self):
        return f"order_id={self.order_id} date={self.order_date} amount={self.amount} type={self.type}"

                
