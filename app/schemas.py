from pydantic import BaseModel, field_validator, model_validator
import uuid
from datetime import date
from fastapi import UploadFile, HTTPException, status
import re,os
from typing import List
import datetime

def validate_password(value):
    if len(value) < 6:
        raise ValueError('Password must be at least 6 characters long')

    if not re.search(r'[A-Za-z]', value):  # Check for at least one letter
        raise ValueError('Password must include at least one letter')

    if not re.search(r'\d', value):  # Check for at least one number
        raise ValueError('Password must include at least one number')
    return value




class Base(BaseModel):
    pass



#  Schemas for Todo


class TodoModelUpdate(BaseModel):
    title:str
    content:str
    completed:bool
    updated_at:datetime.datetime
    class Config:
        extra = 'forbid'


class TodoModelCreate(TodoModelUpdate):
    created_at:datetime.datetime
  
 
class TodoModelResponse(TodoModelCreate):
    todo_id:uuid.UUID 
    user_id:uuid.UUID






# schemas for User


class UserModelSignUp(BaseModel):
    username: str
    password: str
    confirm_password:str

    @field_validator('password')
    @classmethod
    def check_passowrd(cls,value):
        return validate_password(value)

    

    @model_validator(mode="before")
    @classmethod
    def validate(cls,values):
        if values.get("password") != values.get("confirm_password"):
            raise ValueError("Passwords do not match")
        return values
    

class UserModelUpdate(BaseModel):
    date_of_birth: date
    user_img: UploadFile   
    user_cv: UploadFile  
    

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls,value):
        accepted_date = date(1950,1,1)
        if value < accepted_date:
            raise HTTPException(status_code=400, detail=f'date of birth can not be less than 01-01-1950')
        return value




    # Validator for user image (image file)
    @field_validator('user_img')
    @classmethod
    def validate_user_img(cls, value):
        if value:
            ext = os.path.splitext(value.filename)[1][1:].lower()  # Get the extension from the filename
            allowed_image_extensions = {'jpeg', 'jpg', 'png'}  # Acceptable image file types
            if ext not in allowed_image_extensions:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='Only jpeg, jpg, and png files are allowed for images.')
        return value
    
    # Validator for user CV (CV file)
    @field_validator("user_cv")
    def validate_user_cv(cls, value: UploadFile):
        allowed_cv_extensions = ["pdf", "txt"]  # Acceptable CV file types
        ext = value.filename.split(".")[-1].lower()  # Extract extension from filename
        if ext not in allowed_cv_extensions:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail= "Only PDF and TXT files are allowed for CVs")
        return value

class UserModelResponse(BaseModel):
    user_id:uuid.UUID
    username: str
    date_of_birth: date | None
    user_img: str | None 
    user_cv: str  | None
    todos:List['TodoModelResponse'] = []
     
 
class Token(BaseModel):
    access_token:str
    token_type:str

class UpdatePassword(BaseModel):
    password:str
    confirm_password:str
    
    @field_validator('password')
    @classmethod
    def check_password(cls, value):
        return validate_password(value)

    @model_validator(mode="before")
    @classmethod
    def validate_password(cls,values):
        if values.get('password') != values.get('confirm_password'):
            raise ValueError('Passwords do not match')
        return values



 