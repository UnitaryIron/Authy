from fastapi import FastAPI
from app.routes.auth import router as auth_router

app = FastAPI(title="Authy API", description="Simple Authentication System")

app.include_router(auth_router, prefix="/auth", tags=["authentication"])

@app.get("/")
async def root():
    return {"message": "Authy API is running!"}
    
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
