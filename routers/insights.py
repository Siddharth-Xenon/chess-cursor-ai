from fastapi import APIRouter, HTTPException, Body, Depends
from models.insight import InsightModel
from config.db import db
from bson import ObjectId
from auth.firebase_auth import verify_id_token

router = APIRouter()


# Dependency to verify Firebase ID token and get user information
async def get_current_user(token: str = Depends(verify_id_token)):
    return token


@router.post("/", response_description="Add new insight")
async def create_insight(
    insight: InsightModel = Body(...), user=Depends(get_current_user)
):
    insight = dict(insight)
    insight["game_id"] = ObjectId(insight["game_id"])  # Ensure game_id is ObjectId
    new_insight = await db["insights"].insert_one(insight)
    created_insight = await db["insights"].find_one({"_id": new_insight.inserted_id})
    return created_insight


@router.get("/{id}", response_description="Get a single insight")
async def show_insight(id: str, user=Depends(get_current_user)):
    if (insight := await db["insights"].find_one({"_id": ObjectId(id)})) is not None:
        return insight
    raise HTTPException(status_code=404, detail=f"Insight {id} not found")


@router.get("/game/{game_id}", response_description="Get insights for a game")
async def get_insights_for_game(game_id: str, user=Depends(get_current_user)):
    insights = await db["insights"].find({"game_id": ObjectId(game_id)}).to_list(1000)
    if insights:
        return insights
    raise HTTPException(status_code=404, detail=f"No insights found for game {game_id}")


@router.put("/{id}", response_description="Update an insight")
async def update_insight(
    id: str, insight: InsightModel = Body(...), user=Depends(get_current_user)
):
    insight = {k: v for k, v in insight.dict().items() if v is not None}

    if len(insight) >= 1:
        update_result = await db["insights"].update_one(
            {"_id": ObjectId(id)}, {"$set": insight}
        )

        if update_result.modified_count == 1:
            if (
                updated_insight := await db["insights"].find_one({"_id": ObjectId(id)})
            ) is not None:
                return updated_insight

    if (
        existing_insight := await db["insights"].find_one({"_id": ObjectId(id)})
    ) is not None:
        return existing_insight

    raise HTTPException(status_code=404, detail=f"Insight {id} not found")


@router.delete("/{id}", response_description="Delete an insight")
async def delete_insight(id: str, user=Depends(get_current_user)):
    delete_result = await db["insights"].delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return {"message": "Insight deleted successfully"}

    raise HTTPException(status_code=404, detail=f"Insight {id} not found")
