from pymongo import MongoClient

def get_db():
    client = MongoClient('mongodb+srv://<username>:<password>@<cluster>/test')
    db = client['db_name']
    return db