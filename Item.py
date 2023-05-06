class Item:
    
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
    
    def __str__(self):
        return f"{self.id} for {str(self.name).ljust(12)}Price AUD {self.price}"

        