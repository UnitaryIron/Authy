from fastapi import APIRouter, HTTPException, Depends
from app.models.user import UserCreate, UserLogin, UserResponse
from app.utils.auth import hash_password, verify_password, create_access_token
from app.utils.database import db
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """
    Register a new user with email and password
    """
    try:
        existing_user = db.get_user_by_email(user_data.email)
        if existing_user:
            logger.warning(f"Registration attempt with existing email: {user_data.email}")
            raise HTTPException(
                status_code=400, 
                detail="Email already registered"
            )
        
        hashed_password = hash_password(user_data.password)
        user = db.create_user(user_data.email, hashed_password)
        
        logger.info(f"New user registered: {user_data.email} (ID: {user['id']})")
        return UserResponse(**user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error for {user_data.email}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error during registration"
        )

@router.post("/login")
async def login(user_data: UserLogin):
    """
    Authenticate user and return JWT token
    """
    try:
        user = db.get_user_by_email(user_data.email)
        if not user:
            logger.warning(f"Login attempt with non-existent email: {user_data.email}")
            raise HTTPException(
                status_code=401, 
                detail="Invalid credentials"
            )
        
        if not verify_password(user_data.password, user["hashed_password"]):
            logger.warning(f"Failed login attempt for: {user_data.email}")
            raise HTTPException(
                status_code=401, 
                detail="Invalid credentials"
            )
        
        access_token = create_access_token(data={"sub": str(user["id"])})
        
        logger.info(f"Successful login: {user_data.email} (ID: {user['id']})")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(**user)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for {user_data.email}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error during login"
        )

@router.post("/forgot-password")
async def forgot_password(email: str):
    """
    Initiate password reset process
    """
    return {
        "message": "If the email exists, a reset link has been sent",
        "status": "success"
    }
