from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy import insert ,select, delete,update
from models import User
from passlib.context import CryptContext
from schemas import  (UserModelSignUp,
                       UserModelUpdate,
         UpdatePassword, TodoModelResponse, UserModelResponse)
from models import User,Todo
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
import jwt
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
import os, shutil

pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/sign_in')
SECRET_KEY = '2093jfmawj0d92093jf029)*)H)fj-290fsldifj3209jf'
ALGORITHM = 'HS256'

 

def authenticate_user(username:str,password:str,session:Session):
    stmt = select(User).where(User.username==username)
    user = session.execute(stmt).scalar()
    if not user:
        return False
    if not pwd_context.verify(password,user.password):
        return False
    return user


def create_access_token(expires_delta:timedelta,data: dict):
    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expires})  
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    return username





def get_all_users(session: Session):
    users = session.execute(
        select(User)
        .options(joinedload(User.todos))  
    ).unique().scalars().all()  
    
    return users


def sign_up(user_data:UserModelSignUp,session:Session):
    stmt = insert(User).values(
        username=user_data.username,
        password=pwd_context.hash(user_data.password))
    session.execute(stmt)
    session.commit()
    return {'success':'your account has been created'}





def update_user_data(
        user_data:UserModelUpdate,
        username: str, 
        session: Session):

    stmt = select(User).where(User.username == username)
    user = session.execute(stmt).scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    UPLOAD_DIR = "uploads"
    IMG_DIR = os.path.join(UPLOAD_DIR, "images", username)
    CV_DIR = os.path.join(UPLOAD_DIR, "cv", username)

    # Ensure directories exist
    for directory in [UPLOAD_DIR, IMG_DIR, CV_DIR]:
        os.makedirs(directory, exist_ok=True)

    cv_path = os.path.join(CV_DIR, user_data.user_cv.filename)
    with open(cv_path, "wb") as buffer:
        shutil.copyfileobj(user_data.user_cv.file, buffer)

    # Save Image
    img_path = os.path.join(IMG_DIR, user_data.user_img.filename)
    with open(img_path, "wb") as buffer:
        shutil.copyfileobj(user_data.user_img.file, buffer)

    # Update User Model
    user.user_cv = cv_path
    user.user_img = img_path    
    user.date_of_birth = user_data.date_of_birth
    session.commit()

    return {"message": "Data updated successfully"}


def remove_account(user:User,session:Session):
    stmt = delete(User).where(User.username==user)
    user = session.execute(stmt)
    session.commit()
    if not user:
        return False
    return {'success':'account removed'}


 


def update_password(
        user:User,
        data:UpdatePassword,
        session:Session,
        ):
    stmt = select(User).where(User.username==user)
    user = session.execute(stmt).scalar()
    if not user:
        return False
    user.password = pwd_context.hash(data.password)
    session.commit()

 

    return {'success':'password updated'}
    


