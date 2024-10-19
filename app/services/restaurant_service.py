from app.db.mongo import collection
from app.models.restaurant import RestaurantData

from typing import List, Dict

async def get_restaurant_data(restaurant_id: str) -> RestaurantData:
    doc = await collection.find_one({"restaurant_id": restaurant_id})

    if doc:
        doc_data = {
            **doc,
            "_id": str(doc.get("_id")),
        }
        print(doc_data)
        return RestaurantData(**doc_data)
    else:
        return RestaurantData(name="", address={"street": "", "city": "", "zipcode": ""})

async def get_restaurants_by_borough(borough: str) -> List[RestaurantData]:
    cursor = collection.find({"borough": borough})
    restaurants = []

    async for doc in cursor:
        doc_data = {
            **doc,
            "_id": str(doc.get("_id")),
        }

        restaurants.append(RestaurantData(**doc_data))

    return restaurants

async def get_all_borough_names() -> list[str]:
    boroughs = await collection.distinct("borough")
    return boroughs

async def total_score_of_restaurant(restaurant_id: str) -> dict:
    pipline = [
        {"$match": {"restaurant_id": restaurant_id}},
        {"$unwind": "$grades"},
        {"$group": {
            "_id": "$resaurant_id",

            "total_score": {"$sum": "$grades.score"}
        }}
    ]

    result = await collection.aggregate(pipline).to_list(length=1)
    score = None

    if result:
       score = result[0]['total_score']

    return {"score": score}

async def restaurants_borough_by_score(borough_name: str) -> List[dict]:
    pipeline = [
        {"$match": {"borough": borough_name}},
        {"$unwind": "$grades"},
        {"$group": {
            "_id": "$_id",
            "restaurant_id": {"$first": "$restaurant_id"},
            "name": {"$first": "$name"},
            "cuisine": {"$first": "$cuisine"},
            "total_score": {"$sum": "$grades.score"}
        }},
        {"$match": {
            "total_score": {"$gte": 50, "$lte": 100}
        }},
        {"$project": {
            "_id": 0,
            "restaurant_id": 1,
            "name": 1,
            "cuisine": 1,
            "total_score": 1
        }},
        {"$sort": {"total_score": -1}}
    ]
    results = await collection.aggregate(pipeline).to_list(length=None)


    return results
