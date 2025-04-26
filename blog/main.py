import config, models, utils, schema, auth
from database import engine, sessionLOCAL, Base
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = sessionLOCAL()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schema.Userresponse)
def register(user: schema.Usercreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = utils.hash_password(user.password)

    new_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schema.UserWithToken)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not existing_user or not utils.verify_password(form_data.password, existing_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Generate access token (for short-lived access)
    access_token = utils.create_access_token(data={"sub": existing_user.email})
    
    # Generate refresh token (for long-lived refresh)
    refresh_token = utils.create_refresh_token(data={"sub": existing_user.email})

    return {
        "id": existing_user.id,
        "username": existing_user.username,
        "email": existing_user.email,
        "access_token": access_token,
        "refresh_token": refresh_token,  
        "token_type": "bearer"
    }


@app.post("/refresh_token", response_model=schema.UserWithToken)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = utils.verify_refresh_token(refresh_token)
    user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = utils.create_access_token(data={"sub": user.email})

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/create_blog", response_model=schema.Blogresponse)
def create_blog(blog: schema.Blogcreate, db: Session = Depends(get_db), token: str = Depends(auth.oauth_token)):
    payload = utils.verify_access_token(token)
    user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")   
    
    new_blog = models.BlogPost(title=blog.title, content=blog.content, author_id=user.id)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog  


@app.get("/get_blogs", response_model=list[schema.Blogresponse])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.BlogPost).all()
    if not blogs:
        raise HTTPException(status_code=404, detail="No blogs found")
    
    return blogs

@app.get("/getblogs/{blog_id}", response_model=schema.Blogresponse)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.BlogPost).filter(models.BlogPost.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.put("/update_blogs/{blog_id}", response_model=schema.Blogresponse)
def update_blog(blog_id: int, blog: schema.Blogcreate, db: Session = Depends(get_db), token: str = Depends(auth.oauth_token)):
    payload = utils.verify_access_token(token)

    user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    blog_entry = db.query(models.BlogPost).filter(models.BlogPost.id == blog_id, models.BlogPost.author_id == user.id).first()

    if not blog_entry:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    blog_entry.title = blog.title
    blog_entry.content = blog.content
    db.commit()
    db.refresh(blog_entry)

    return blog_entry

@app.delete("/delete_blog/{blog_id}", response_model=dict)
def delete_blog(blog_id: int, db: Session = Depends(get_db), token: str = Depends(auth.oauth_token)):
    payload = utils.verify_access_token(token)
    user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    blog = db.query(models.BlogPost).filter(models.BlogPost.id == blog_id, models.BlogPost.author_id == user.id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}
