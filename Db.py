from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://MainakGhosh:Admin123@cluster0.xkfqmh9.mongodb.net/?retryWrites=true&w=majority")
db = cluster["EducationManagmentSystem"]


# collection = db['Student']
# result = collection.find({"roll": 24})
# print(result)
# for x in result:
#     print(x)

def insert(post, collection):
    collection = db[collection]
    collection.insert(post)


def insert_one(post, collection):
    collection = db[collection]
    collection.insert_one(post)


def find(post, collection):
    collection = db[collection]
    result = collection.find(post)
    return result


def find_one(post, collection):
    collection = db[collection]
    result = collection.find_one(post)
    return result


def delete(post, collection):
    collection = db[collection]
    collection.delete_many(post)


def delete_one(post, collection):
    collection = db[collection]
    collection.delete_one(post)