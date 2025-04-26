from pydantic import BaseModel,EmailStr

class DocumentCreate(BaseModel):
    document_name:str
    document_type:str
    owner_id:int
    
class DocumentResponse(BaseModel):
    document_id:int
    document_name:str
    document_type:str
    owner_id:int

    class Config:
        orm_mode=True

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr

    class Config:
        orm_mode=True

