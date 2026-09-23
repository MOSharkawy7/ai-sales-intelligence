from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import (
    sales,
    customers,
    anomalies,
)


app = FastAPI(
    title="AI Sales Intelligence API",
    description=(
        "REST API for sales analytics, "
        "forecasting, customer segmentation, "
        "and anomaly detection."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    sales.router
)

app.include_router(
    customers.router
)

app.include_router(
    anomalies.router
)


@app.get("/")
def root():

    return {
        "message": "AI Sales Intelligence API",
        "status": "running",
    }


@app.get("/api/health")
def health_check():

    return {
        "status": "healthy"
    }