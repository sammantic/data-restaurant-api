from fastapi import APIRouter
from typing import List, Dict

from app.services.restaurant_service \
    import  get_restaurant_data, \
            get_restaurants_by_borough, \
            get_all_borough_names, \
            total_score_of_restaurant, \
            restaurants_borough_by_score



from app.models.restaurant import RestaurantData

router = APIRouter()

@router.get("/restaurants/boroughs", response_model=list[str])
async def read_all_borough_names():
    boroughs = await get_all_borough_names()
    return boroughs

@router.get("/restaurants/{restaurant_id}", response_model=RestaurantData)
async def read_restaurant(restaurant_id: str):
    restaurant_data = await get_restaurant_data(restaurant_id)
    return restaurant_data

@router.get("/restaurants/{restaurant_id}/score", response_model=dict)
async def read_total_score_restaurant(restaurant_id: str):
    restaurant_score = await total_score_of_restaurant(restaurant_id)
    return restaurant_score

@router.get("/restaurants/borough/{borough}")
async def read_restaurants_by_borough(borough: str, response_model=List[RestaurantData]):
    restaurants = await get_restaurants_by_borough(borough)
    return restaurants

@router.get("/restaurants/borough/{borough_name}/score", response_model=list[dict])
async def read_restaurants_brough_by_score(borough_name: str):
    restaurant_by_score = await restaurants_borough_by_score(borough_name)
    return restaurant_by_score

