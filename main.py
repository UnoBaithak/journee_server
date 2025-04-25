from fastapi import FastAPI
from routes import router as app_router
from dotenv import load_dotenv

load_dotenv("development.env")

app = FastAPI()

app.include_router(app_router, prefix="/api")

@app.get("/")
def home():
    return {"message": "Welcome to Athena"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8090)