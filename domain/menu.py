class menu:
    def __init__(self):
        self.menu = {
            '1': 'Add',
            '2': 'Subtract',
            '3': 'Multiply',
            '4': 'Divide',
            '5': 'Exit'
        }

    def display_menu(self):
        for key, value in self.menu.items():
            print(f'{key}: {value}')

    def get_menu(self):
        return self.menu