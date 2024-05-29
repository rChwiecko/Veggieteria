from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db = client['mydatabase']

users = db["users"]

ex_data = {
    "first_name": "Ryan",
    "last_name":"Chwiecko",
    "user_name": "rChwiecko",
    "password": "123",
    "coin_count": 0
}

def insertData(data):
    try:
        if get_data(data["user_name"]) is not None:
            raise Exception("User with name exists already")
        result = users.insert_one({"first_name": data["first_name"], "last_name": data["last_name"], "user_name": data["user_name"], "passowrd": data["password"], "coin_count": data["coin_count"]})
        return result
    except:
        return False

def get_data(username):
    try:
        user = users.find_one({"user_name": username})
        return user
    except:
        return False
    
def update_coin_count(username, count):
    try:
        if get_data(username) is not None:
            raise Exception("User with name exists already")
        result = users.update_many({"users.user_name": username}, {"$set": {"users.$.coin_count": count}})
        return result    
    except:
        return False


insertData(ex_data)