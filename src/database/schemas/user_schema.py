from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str
    company_name: str = None


class ShowUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    company_name: str

    class Config:
        orm_mode = True
