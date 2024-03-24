from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import users, games, insights
from config.db import close_mongo_connection, connect_to_mongo
from auth.firebase_auth import verify_id_token

app = FastAPI()

# CORS middleware configuration
origins = [
    "http://localhost:3000",  # Assuming the React frontend runs on localhost:3000
    "https://your-deployment-domain.com",  # Update this with your actual deployment domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database event handlers
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


# Dependency to verify Firebase ID token
def get_current_user(token: str = Depends(verify_id_token)):
    return token


# Including routers
app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_current_user)],
)
app.include_router(
    games.router,
    prefix="/games",
    tags=["games"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    insights.router,
    prefix="/insights",
    tags=["insights"],
    dependencies=[Depends(get_current_user)],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Chess Tutor API!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
