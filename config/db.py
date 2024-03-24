from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()  # This method call loads the environment variables


class DataBase:
    client: AsyncIOMotorClient = None


def get_database():
    return DataBase.client["chess-tutor"]


async def connect_to_mongo():
    print(os.getenv("MONGODB_URL"))
    DataBase.client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    # DataBase.client = AsyncIOMotorClient(
    #     "mongodb+srv://sidsolanki920:ApoI4UMIy5HUgdHp@chess-tutor.tdk16xb.mongodb.net/chess-tutor"
    # )


async def close_mongo_connection():
    DataBase.client.close()


def create_app():
    app = FastAPI()
    app.add_event_handler("startup", connect_to_mongo)
    app.add_event_handler("shutdown", close_mongo_connection)

    return app


db = DataBase.client
