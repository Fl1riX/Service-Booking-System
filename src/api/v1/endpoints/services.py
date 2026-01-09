import schemas

from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import models

router = APIRouter(prefix="/services", tags=["Услуги"])

@router.get("/{service_id}", response_model=schemas.ServiceResponse)
async def get_service(service_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Service).where(
        models.Service.id == service_id
    ))
    service = result.scalars().first()
    if not service:
        raise HTTPException(status_code=404, detail="Такая услуга не найдена")
    return service

@router.post("/", response_model=schemas.ServiceResponse)
async def create_service(service: schemas.ServiceCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Service).where(
        models.Service.name == service.name,
        models.Service.entrepreneur_id == service.entrepreneur_id
    ))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Такая услуга уже существует")
    
    new_service = models.Service(**service.dict())
    
    db.add(new_service)
    await db.commit()
    await db.refresh(new_service)
    
    return new_service

@router.delete("/{service_id}", response_model=schemas.ServiceResponse)
async def delete_service(service_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Service).where(
        models.Service.id == service_id
    ))
    service = result.scalars().first()
    
    if not service:
        raise HTTPException(status_code=404, detail="Такой услуги не существует")
    
    await db.delete(service)
    await db.commit()
    
@router.put("/{service_id}", response_model=schemas.ServiceResponse)
async def update_service(new_service: schemas.ServiceCreate, service_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Service).where(
        models.Service.id == service_id
    ))
    service = result.scalars().first()
    
    if not service:
        raise HTTPException(status_code=404, detail="Такоая услуга не найдена")
    
    for key, value in new_service.dict().items():
        if hasattr(key, service) and value is not None:
            setattr(service, key, value)
    
    await db.commit()
    await db.refresh(service)