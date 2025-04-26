from pydantic import BaseModel, EmailStr

class Usercreate(BaseModel):
    username:str
    email:EmailStr
    password:str

    class Config:
        orm_mode=True

class Userresponse(BaseModel):
    id:int
    username:str
    email:EmailStr

    class Config:
        orm_mode=True

