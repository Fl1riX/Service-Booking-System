import schemas

from db import models
from db.database import get_db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/entrepreneurs", tags=["Предприниматели"])

@router.get("/{user_id}", response_model=schemas.EntrepreneurResponse)
async def get_user(user_id:  int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Entrepreneur).where(
        models.Entrepreneur.id == user_id
    ))
    entrepreneur = result.scalars().first()
    if not entrepreneur:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return entrepreneur

@router.post("/", response_model=schemas.EntrepreneurResponse)
async def create_entrepreneur(enterpreneur: schemas.EntrepreneurCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Entrepreneur).where(
        models.Entrepreneur.telegram_id == enterpreneur.telegram_id
    ))
    existing = result.scalars().first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Такой пользователь уже существует")
    
    new_entrepreneur = models.Entrepreneur(**enterpreneur.dict())
    
    db.add(new_entrepreneur)
    await db.commit()
    await db.refresh(new_entrepreneur)
    
    return new_entrepreneur

@router.put("/{entrepreneur_id}", response_model=schemas.EntrepreneurResponse)
async def update_entrepreneur(entrepreneur_id: int, db: AsyncSession = Depends(get_db)):
    pass