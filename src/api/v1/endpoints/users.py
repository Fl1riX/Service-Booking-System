import schemas

from db.database import get_db
from db import models
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(
        models.User.id == user_id
    )) 
    user = result.scalars().first() 
    if not user:
        raise HTTPException(status_code=404, detail=f"Пользователь не найден")
    return user

@router.post("/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(
        models.User.telegram_id == user.telegram_id
    ))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Такой пользователь уже существует")
    new_user = models.User(**user.dict())
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_user(user_id: int, new_user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(
        models.User.id == user_id
    ))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Нельзя обновить даные. Такого пользователя не существует")
    
    # построчно передираем словарь
    for key, value in new_user.dict().items(): # items построчно разбивает словрь на пары (ключ, значение)
        if hasattr(user, key) and value is not None: # если в user(в бд) есть такое поле
            setattr(user, key, value)                # то задаем значение для поля 
    
    await db.commit()
    await db.refresh(user)
    
    return user

@router.delete("/{user_id}", status_code=204)
async def delet_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(
        models.User.id == user_id
    ))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Такого пользователя не существует")
    
    await db.delete(user)
    await db.commit()
    