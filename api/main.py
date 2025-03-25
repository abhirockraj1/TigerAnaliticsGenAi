# app/api/main.py
from fastapi import FastAPI
from api.endpoints import user
from api.utils.database import engine, Base

app = FastAPI()

app.include_router(user.router, prefix="/api/v1")

# Create database tables on startup
def create_tables():
    Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup_event():
    create_tables()
# You would include other routers here as well
# from app.api.endpoints import code_file, collaboration, ai_debugging
# app.include_router(code_file.router, prefix="/api/v1")
# app.include_router(collaboration.router, prefix="/api/v1")
# app.include_router(ai_debugging.router, prefix="/api/v1")