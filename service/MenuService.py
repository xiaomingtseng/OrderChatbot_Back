from domain.menu import Menu, MenuItem
from infrastructure.menuRepo import MenuRepository
from bson import ObjectId

class MenuService:
    def __init__(self, menu_repo: MenuRepository):
        self.menu_repo = menu_repo

    def create_menu(self, menu: Menu):
        return self.menu_repo.add_menu(menu)

    def get_menu(self, menu_id: str):
        return self.menu_repo.get_menu_by_id(ObjectId(menu_id))

    def update_menu(self, menu_id: str, update_data: dict):
        return self.menu_repo.update_menu(ObjectId(menu_id), update_data)

    def delete_menu(self, menu_id: str):
        return self.menu_repo.delete_menu(ObjectId(menu_id))

    def create_menu_item(self, menu_item: MenuItem):
        return self.menu_repo.add_menu_item(menu_item)

    def get_menu_item(self, menu_item_id: str):
        return self.menu_repo.get_menu_item_by_id(ObjectId(menu_item_id))
    
    def add_menu_item_to_menu(self, menu_id: str, menu_item_id: str):
        return self.menu_repo.add_item_to_menu(ObjectId(menu_id), ObjectId(menu_item_id))
    
    def remove_menu_item_from_menu(self, menu_id: str, menu_item_id: str):
        return self.menu_repo.remove_item_from_menu(ObjectId(menu_id), ObjectId(menu_item_id))

    def update_menu_item(self, menu_item_id: str, update_data: dict):
        return self.menu_repo.update_menu_item(ObjectId(menu_item_id), update_data)

    def delete_menu_item(self, menu_item_id: str):
        return self.menu_repo.delete_menu_item(ObjectId(menu_item_id))