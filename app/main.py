from fastapi import FastAPI
from routes.user_api import router as user_router
from routes.todo_api import router as todo_router


app = FastAPI()


app.include_router(user_router)
app.include_router(todo_router)
