from pymongo import MongoClient


class Database():
    def __init__(self):
        self.client = MongoClient(
            'mongodb+srv://Petr:GPpetr1309@cluster0-nli2o.mongodb.net/test?retryWrites=true&w=majority')
        self.db = self.client['Olympbot']
        self.users = self.db.Users

    def add_user(self, user):
        self.users.insert_one(user)

    def check_in_users(self, user):
        return self.users.find_one({'id': user['id']})
    def delete_user(self, user):
        self.users.delete_one({'id': user['id']})
        return True
    def get_user(self, user_id):
        return self.users.find_one({'id': user_id})
