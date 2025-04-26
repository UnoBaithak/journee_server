from fastapi import FastAPI
from routes import AuthRouter, ItineraryRouter, UserRouter

app = FastAPI()

app.include_router(AuthRouter)
app.include_router(ItineraryRouter)
app.include_router(UserRouter)

@app.get("/")
def home():
    return {"message": "Welcome to Athena"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8090)