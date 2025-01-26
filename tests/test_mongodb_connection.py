import pytest
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

def test_mongodb_connection():
    try:
        # 嘗試連接到 MongoDB
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
    except ServerSelectionTimeoutError:
        pytest.fail("Could not connect to MongoDB")

def test_insert_and_find():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['test_database']
    collection = db['test_collection']

    # 插入測試文檔
    test_document = {'name': 'test', 'value': 123}
    collection.insert_one(test_document)

    # 查找插入的文檔
    found_document = collection.find_one({'name': 'test'})
    assert found_document is not None
    assert found_document['value'] == 123

    # 清理測試數據
    collection.delete_many({})
    client.drop_database('test_database')