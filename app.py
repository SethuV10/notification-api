from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from repositories.database import init_db

from controllers.auth_controller import router as auth_router
from controllers.user_controller import router as user_router
from controllers.room_controller import router as room_router
from controllers.message_controller import router as message_router
from controllers.team_controller import router as team_router
from controllers.staff_controller import router as staff_router
from controllers.category_controller import router as category_router
from controllers.role_controller import router as role_router


app = FastAPI(
    title="Office Call Notification System",
    version="0.1.0",
)

# Configure CORS for local frontend development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all application routers.
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(room_router)
app.include_router(message_router)
app.include_router(team_router)
app.include_router(staff_router)
app.include_router(category_router)
app.include_router(role_router)


# Initialize the database.
init_db()


@app.get("/")
def root():
    return {"message": "Hello"}


@app.get("/ping")
def ping():
    return {"status": "ok"}
