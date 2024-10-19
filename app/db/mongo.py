from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB setup
client = AsyncIOMotorClient("mongodb://root:example@localhost:27017/restranutes?retryWrites=true&writeConcern=majority&authSource=admin")
db = client["restranunts"]
collection = db['restaurant']