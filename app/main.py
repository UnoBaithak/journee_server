from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import AuthRouter, ItineraryRouter, UserRouter

app = FastAPI()

origins = [
    "https://*.vercel.app",  # replace with your actual frontend domain
]

# Apply CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # only this domain is allowed
    allow_credentials=True,
    allow_methods=["*"],            # you can limit to ['GET', 'POST'] if needed
    allow_headers=["*"],
)

app.include_router(AuthRouter)
app.include_router(ItineraryRouter)
app.include_router(UserRouter)

@app.get("/")
def home():
    return {"message": "Welcome to Athena"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8090)