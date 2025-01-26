class CartRepository:
    def __init__(self):
        self.cart = []

    def add(self, item):
        self.cart.append(item)

    def remove(self, item):
        self.cart.remove(item)

    def get(self):
        return self.cart

    def clear(self):
        self.cart = []