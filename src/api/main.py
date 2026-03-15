from fastapi import FastAPI

from api.database import Base, engine
from api.routes import router

app = FastAPI(title="Notes API")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(router)