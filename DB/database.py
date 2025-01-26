from pymongo import MongoClient

class Database:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

# 使用範例
db = Database('mongodb://localhost:27017/', 'mydatabase')
collection = db.get_collection('mycollection')