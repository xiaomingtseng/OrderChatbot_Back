class Cart:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def remove(self, item):
        self.items.remove(item)

    def get_total(self):
        return sum([item.price for item in self.items])

    def get_items(self):
        return self.items