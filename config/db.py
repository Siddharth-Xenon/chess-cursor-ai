from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
import os


class DataBase:
    client: AsyncIOMotorClient = None


def get_database():
    return DataBase.client["chess-tutor"]


async def connect_to_mongo():
    DataBase.client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))


async def close_mongo_connection():
    DataBase.client.close()


def create_app():
    app = FastAPI()
    app.add_event_handler("startup", connect_to_mongo)
    app.add_event_handler("shutdown", close_mongo_connection)

    return app


db = DataBase.client
