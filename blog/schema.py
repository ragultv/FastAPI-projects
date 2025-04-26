from pydantic import BaseModel, EmailStr

class Usercreate(BaseModel):
    username: str
    email: str
    password: str

    class Config:  
        orm_mode = True

class Userresponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:  
        orm_mode = True

class UserWithToken(Userresponse):
    access_token: str
    token_type: str

class Blogcreate(BaseModel):
    title: str
    content: str

    class Config:  
        orm_mode = True
    
class Blogresponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int

    class Config:  
        orm_mode = True
