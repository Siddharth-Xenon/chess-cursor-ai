from fastapi import APIRouter, HTTPException, Body, Depends
from models.game import GameModel
from config.db import db
from bson import ObjectId
from auth.firebase_auth import verify_id_token

router = APIRouter()


# Dependency to verify Firebase ID token and get user information
async def get_current_user(token: str = Depends(verify_id_token)):
    return token


@router.post("/", response_description="Add new game")
async def create_game(game: GameModel = Body(...), user=Depends(get_current_user)):
    game = dict(game)
    game["user_id"] = ObjectId(user["uid"])  # Convert user UID to ObjectId
    new_game = await db["games"].insert_one(game)
    created_game = await db["games"].find_one({"_id": new_game.inserted_id})
    return created_game


@router.get("/{id}", response_description="Get a single game")
async def show_game(id: str, user=Depends(get_current_user)):
    if (
        game := await db["games"].find_one(
            {"_id": ObjectId(id), "user_id": ObjectId(user["uid"])}
        )
    ) is not None:
        return game
    raise HTTPException(status_code=404, detail=f"Game {id} not found")


@router.put("/{id}", response_description="Update a game")
async def update_game(
    id: str, game: GameModel = Body(...), user=Depends(get_current_user)
):
    game = {k: v for k, v in game.dict().items() if v is not None}

    if len(game) >= 1:
        update_result = await db["games"].update_one(
            {"_id": ObjectId(id), "user_id": ObjectId(user["uid"])}, {"$set": game}
        )

        if update_result.modified_count == 1:
            if (
                updated_game := await db["games"].find_one({"_id": ObjectId(id)})
            ) is not None:
                return updated_game

    if (existing_game := await db["games"].find_one({"_id": ObjectId(id)})) is not None:
        return existing_game

    raise HTTPException(status_code=404, detail=f"Game {id} not found")


@router.delete("/{id}", response_description="Delete a game")
async def delete_game(id: str, user=Depends(get_current_user)):
    delete_result = await db["games"].delete_one(
        {"_id": ObjectId(id), "user_id": ObjectId(user["uid"])}
    )

    if delete_result.deleted_count == 1:
        return {"message": "Game deleted successfully"}

    raise HTTPException(status_code=404, detail=f"Game {id} not found")
