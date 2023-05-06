
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
