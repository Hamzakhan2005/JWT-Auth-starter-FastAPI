from fastapi import APIRouter, Depends, HTTPException
from schemas.user_schema import UserRegister, UserLogin
from schemas.token_schema import Token
from controllers.auth_controller import AuthController
from middleware.auth_middleware import get_current_user, get_current_admin
from models.user import UserRole

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", status_code=201)
async def register(user_data: UserRegister):
    """Register a new user"""
    return await AuthController.register(user_data)

@router.post("/login")
async def login(login_data: UserLogin):
    """Login user"""
    return await AuthController.login(login_data)

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current logged in user (Protected Route)"""
    return await AuthController.get_current_user_info(current_user)

@router.get("/admin")
async def admin_only(current_user: dict = Depends(get_current_admin)):
    """Admin only route (Protected Route)"""
    return {
        "success": True,
        "message": "Welcome Admin!",
        "user": {
            "id": str(current_user["_id"]),
            "name": current_user["name"],
            "email": current_user["email"],
            "role": current_user["role"]
        }
    }