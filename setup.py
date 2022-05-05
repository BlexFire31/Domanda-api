from pymongo import MongoClient

client=MongoClient("mongodb://mongo:27017/")

# create schemas

client.data.create_collection("quizzes",{
    "validator":{
        "$jsonSchema":{
            "bsonType":"object",
            "required":["id","state","active","users","members","questions"],
            "properties":{
                "id":{
                    "bsonType":"int",
                    "minimum":1,
                    "description":"Number identifier for the quiz"
                },
                "state":{
                    "enum":["ACTIVE","INACTIVE"],
                    "description":"Current state of the quiz",
                },
                "active":{
                    "bsonType":"int",
                    "minimum":0,
                    "description":"If the quiz is active, this field specifies which quiz is currently active",
                },
                "users":{
                    "bsonType":"object",
                    "properties":
                }
            }
        }
    }
})