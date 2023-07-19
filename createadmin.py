import pymongo

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["feedback"]
collection = db["reviews"]

# Add admin user
admin_user = {
    "username": "adii",
    "password": "addy",
    "role": "admin"
}

collection.insert_one(admin_user)
