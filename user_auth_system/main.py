from fastapi import FastAPI, Depends, HTTPException, status
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import engine ,sessionLOCAL, Base
import models,schema,utils,auth
Base.metadata.create_all(bind=engine)

app=FastAPI()

def get_db():
    db=sessionLOCAL()
    try:
        yield db
    finally:
        db.close()

@app.post("/register",response_model=schema.Userresponse)
def register(user:schema.Usercreate,db:Session=Depends(get_db)):

    existing_user=db.query(models.user).filter(models.user.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail=('email already registered'))

    hashed_password=utils.hash_password(user.password)

    new_user=models.user(username=user.username,email=user.email,password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/admin_register",response_model=schema.Userresponse)
def admin_register(admin:schema.Usercreate,db:Session=Depends(get_db)):
    existing_admin=db.query(models.user).filter(models.user.email==admin.email).first()
    if existing_admin:
        raise HTTPException(status_code=400,detail=('email already registered'))

    hashed_password=utils.hash_password(admin.password)

    new_admin=models.user(username=admin.username,email=admin.email,password=hashed_password,role="admin")
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    
    return {"message": f"Admin {new_admin.username} created successfully"}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(models.user).filter(models.user.username == form_data.username).first()

    if not existing_user or not utils.verify_password(form_data.password, existing_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = utils.create_access_token(data={"sub": existing_user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/admin_login")
def admin_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_admin = db.query(models.user).filter(models.user.username == form_data.username).first()

    if not existing_admin or not utils.verify_password(form_data.password, existing_admin.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = utils.create_access_token(data={"sub": existing_admin.email})

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/admin-only")
def admin_only_route(user: models.user = Depends(auth.get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return {"message": "Welcome, Admin!"}

@app.get("/user-only")
def user_only_route(user: models.user = Depends(auth.get_current_user)):
    if user.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return {"message": "Welcome, User!"}

