from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.session import engine
from src.database import Base, settings_config
from src.apis.base import api_router


def create_tables():
    Base.metadata.create_all(bind=engine)

def include_router(app):
    app.include_router(api_router)

def start_application():
    app = FastAPI(title=settings_config.PROJECT_NAME, version=settings_config.PROJECT_VERSION)
    origins = [
        # "http://localhost.tiangolo.com",
        # "https://localhost.tiangolo.com",
        # "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    create_tables()
    include_router(app)
    return app

app = start_application()

@app.get("/healthz")
def read_root():
    return {"message": "success"}
