from fastapi import HTTPException, status
from config.database import get_database
from schemas.user_schema import UserRegister, UserLogin, UserResponse
from schemas.token_schema import Token
from utils.password_utils import hash_password, verify_password
from utils.token_utils import create_access_token
from datetime import datetime

class AuthController:
    @staticmethod
    async def register(user_data: UserRegister) -> dict:
        """Register a new user"""
        db = get_database()
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists with this email"
            )
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Create user document
        user_dict = {
            "name": user_data.name,
            "email": user_data.email,
            "password": hashed_password,
            "role": user_data.role.value,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Insert into database
        result = await db.users.insert_one(user_dict)
        user_id = str(result.inserted_id)
        
        # Generate token
        access_token = create_access_token(
            data={
                "sub": user_id,
                "email": user_data.email,
                "role": user_data.role.value
            }
        )
        
        return {
            "success": True,
            "message": "User registered successfully",
            "token": access_token,
            "user": {
                "id": user_id,
                "name": user_data.name,
                "email": user_data.email,
                "role": user_data.role.value
            }
        }
    
    @staticmethod
    async def login(login_data: UserLogin) -> dict:
        """Login user and return JWT token"""
        db = get_database()
        
        # Find user by email
        user = await db.users.find_one({"email": login_data.email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verify password
        if not verify_password(login_data.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Generate token
        user_id = str(user["_id"])
        access_token = create_access_token(
            data={
                "sub": user_id,
                "email": user["email"],
                "role": user["role"]
            }
        )
        
        return {
            "success": True,
            "message": "Login successful",
            "token": access_token,
            "user": {
                "id": user_id,
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }
    
    @staticmethod
    async def get_current_user_info(user: dict) -> dict:
        """Get current user information"""
        user_id = str(user["_id"])
        return {
            "success": True,
            "user": {
                "id": user_id,
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }