import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import router

app = FastAPI(title="Service Booking System", version="0.0.1", description="Система для бронирования услуг")
app.include_router(router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_headers = ["*"],
    allow_methods = ["*"],
    allow_origins = ["*"],
    allow_credentials=True
)

@app.get("/")
def wellcome():
    return{
        "message": "Добро пожаловать в Service-Booking-System",
        "detail": "Документация http://localhost:8000/docs"
    }

if __name__ == "__main__":
    uvicorn.run(app, port=8000, reload=True)