from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from . import models
# from .database import engine
from .routers import posts,users,authentification,likes

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins=["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(authentification.router)
app.include_router(likes.router)

@app.get("/")
def get_msg():
    return {"message":"this is my first api"}
