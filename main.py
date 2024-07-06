from fastapi import FastAPI
from src.database.session import engine
from src.database import Base, settings_config


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings_config.PROJECT_NAME, version=settings_config.PROJECT_VERSION)
    create_tables()
    return app


app = start_application()


@app.get("/")
def read_root():
    return {"message": "success"}
