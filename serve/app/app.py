import uvicorn
from fastapi import FastAPI

from serve.app.router import api_router

# Declaring our FastAPI instance
app = FastAPI(
    title="Prediction delivery time",
    description="Prediction delivery time with XGboost",
    version="0.0.1",
)

app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
