from fastapi import FastAPI
from app.routes.auth import router as auth_router
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from app.routes.google_oauth import router as google_router
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

load_dotenv() 
app = FastAPI(title="Logify API", description="Simple Authentication System")

app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(google_router, tags=["google-oauth"])

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Logify API is running!"}
    
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
