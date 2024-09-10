from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserCreate(UserLogin):
    first_name: str
    last_name: str
    company_name: str = None


class CompleteInfo(BaseModel):
    purpose: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    company_name: str

    class Config:
        orm_mode = True
