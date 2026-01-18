from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db.database import get_db
from src.api.v1.auth.jwt_handler import decode_token
from src.services.user_service import UserService
from src.logger import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login") # указываем URL эндпоинта логина

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """
    Возвращаем id пользователя, 
    который пытается получить доступ к защищенной ручке, 
    т.е достаем его из заголовков
    """
    
    payload = decode_token(token)

    if not payload:
        logger.warning("Невалидный или истекший токен")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
            headers={"WWW-Auntificate": "Bearer"}
        )
    
    user_id = payload.get("user_id")

    if not user_id:
        logger.warning("В токене отсутствует user_id")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
            headers={"WWW-Auntificate": "Bearer"}
        )
    return user_id

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """Возвращает User из бд"""
    payload = decode_token(token)
    
    if not payload:
        logger.warning("Невалидный или истекший токен")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
            headers={"WWW-Auntificate": "Bearer"}
        )
    
    user_id = payload.get("user_id")
    
    if not user_id:
        logger.warning("Токен не содержит user_id")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
            headers={"WWW-Auntificate": "Bearer"}
        )
    
    user = await UserService.find_user_by_id(id=user_id, db=db)
    
    if not user:
        logger.warning(f"Пользователь с id: {user_id} не найден")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    return user
        
    
    
    
    
    
    


