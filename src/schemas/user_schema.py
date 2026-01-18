from pydantic import BaseModel, ConfigDict, model_validator, Field
from typing import Optional
from .types import TgId, Email, PhoneNumber
from datetime import datetime

class UserRegister(BaseModel):
    telegram_id: TgId | None 
    username: str = Field(max_length=50)
    phone: PhoneNumber | None
    email: Email 
    password: str = Field(max_length=255, min_length=8)
    
    model_config = ConfigDict(extra='forbid') # запрещаем не указанные поля

class UserRegisterResponse(BaseModel):
    user: UserRegister
    token: str
    token_type: str
    
    class Config:
        from_attributes = True
        
class UserUpdate(BaseModel):
    telegram_id: Optional[TgId] = None
    username: Optional[str] = None
    phone: Optional[PhoneNumber] = None
    email: Optional[Email] = None
    
    model_config = ConfigDict(extra='forbid') # запрещаем не указанные поля
class UserLogin(BaseModel):
    telegram_id: Optional[TgId] = None
    email: Optional[Email] = None
    phone: Optional[PhoneNumber] = None
    password: str = Field(max_length=255, min_length=8)
    
    model_config = ConfigDict(extra='forbid')
    
    @model_validator(mode="after")
    def validate_fields_not_none(self):
        if self.telegram_id == None and self.email == None and self.phone == None:
            raise ValueError("Нет данных для логина")
        return self
    
class UserLoginResponse(BaseModel):
    id: int
    access_token: str
    token_type: str
    
    class Config:
        from_attributes = True
        
class UserResponse(BaseModel):
    id: int
    telegram_id: TgId | None
    username: str
    phone: PhoneNumber | None
    email: Email 
    created_at: datetime
    is_entrepreneur: bool
    full_name: str | None
    
    class Config:
        from_attributes = True