# app/main.py
from fastapi import FastAPI
from app.routes.auth import router as auth_router

app = FastAPI(title="Authy API", description="Simple Authentication System")

# Include routes
app.include_router(auth_router, prefix="/auth", tags=["authentication"])

@app.get("/")
async def root():
    return {"message": "Authy API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)