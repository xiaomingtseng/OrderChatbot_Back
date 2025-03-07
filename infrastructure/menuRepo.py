from domain.menu import Menu, MenuItem
from infrastructure.database import Database
from bson import ObjectId

class MenuRepository:
    def __init__(self, db: Database):
        self.menu_collection = db.get_collection('menus')
        self.menu_item_collection = db.get_collection('menu_items')

    def add_menu(self, menu: Menu):
        menu_data = {
            '_id': ObjectId(),
            'image_id': menu.image_id,
            'store_id': menu.store_id,
            'menu_item_ids': menu.menu_item_ids
        }
        self.menu_collection.insert_one(menu_data)
        return menu_data

    def get_menu_by_id(self, menu_id: ObjectId):
        menu_data = self.menu_collection.find_one({'_id': ObjectId(menu_id)})
        if menu_data:
            return Menu(str(menu_data['_id']), menu_data['image_id'], menu_data['store_id'], menu_data['menu_item_ids'])
        return None

    def add_item_to_menu(self, menu_id: ObjectId, menu_item_id: ObjectId):
        result = self.menu_collection.update_one({'_id': ObjectId(menu_id)}, {'$push': {'menu_item_ids': menu_item_id}})
        return result.modified_count > 0
    
    def remove_item_from_menu(self, menu_id: ObjectId, menu_item_id: ObjectId):
        result = self.menu_collection.update_one({'_id': ObjectId(menu_id)}, {'$pull': {'menu_item_ids': menu_item_id}})
        return result.modified_count > 0
    
    def update_menu(self, menu_id: ObjectId, update_data: dict):
        result = self.menu_collection.update_one({'_id': ObjectId(menu_id)}, {'$set': update_data})
        return result.modified_count > 0

    def delete_menu(self, menu_id: ObjectId):
        result = self.menu_collection.delete_one({'_id': ObjectId(menu_id)})
        return result.deleted_count > 0

    def add_menu_item(self, menu_item: MenuItem):
        menu_item_data = {
            '_id': ObjectId(),
            'name': menu_item.name,
            'price': menu_item.price,
            'category': menu_item.category
        }
        self.menu_item_collection.insert_one(menu_item_data)
        return menu_item_data

    def get_menu_item_by_id(self, menu_item_id: ObjectId):
        menu_item_data = self.menu_item_collection.find_one({'_id': ObjectId(menu_item_id)})
        if menu_item_data:
            return MenuItem(
                str(menu_item_data['_id']), menu_item_data['name'], menu_item_data['price'],
                menu_item_data['category']
            )
        return None

    def update_menu_item(self, menu_item_id: ObjectId, update_data: dict):
        result = self.menu_item_collection.update_one({'_id': ObjectId(menu_item_id)}, {'$set': update_data})
        return result.modified_count > 0

    def delete_menu_item(self, menu_item_id: ObjectId):
        result = self.menu_item_collection.delete_one({'_id': ObjectId(menu_item_id)})
        return result.deleted_count > 0
