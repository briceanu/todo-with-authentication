from fastapi import APIRouter,HTTPException, Depends, Body, UploadFile, status, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.db_connection import get_db
import routes.user_logic as user_logic
from schemas import  (UserModelSignUp,
                      UserModelResponse,
                      Token,
                      UserModelUpdate,
                      UpdatePassword)
from models import User
from typing import Annotated, List
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, date
 

router = APIRouter(prefix='/user',tags=['all the routes for the user'])



@router.get('/all' )
async def get_users(
    user:Annotated[User,Depends(user_logic.get_current_user)],
    session:Session=Depends(get_db),
    )-> List[UserModelResponse]:
    try:
        users = user_logic.get_all_users(session)
        return users
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"An error occurred: {str(e)}")




@router.post('/sign_up')
async def create_account(user_data:Annotated[UserModelSignUp,Body()]
                        ,session:Session=Depends(get_db))->dict:
    try:
        users = user_logic.sign_up(user_data,session)
        return users
    except HTTPException:
        raise
    except IntegrityError as e:
        raise HTTPException(status_code=400,
                            detail=f'Integrity error: {str(e.orig)}')
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"An error occurred: {str(e)}")


@router.post('/sign_in')
async def get_access_token(
    form_data:Annotated[OAuth2PasswordRequestForm, Depends()],
    session:Session=Depends(get_db))-> Token:
    unauthoriezed_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid username or password',
                            headers={"WWW-Authenticate": "Bearer"})
    
    user = user_logic.authenticate_user(form_data.username,form_data.password,session)
    if not user:
        raise unauthoriezed_exception

    token = user_logic.create_access_token(timedelta(minutes=30),data={'sub':user.username})
    return {'access_token':token,'token_type':'bearer'}


 



@router.patch('/update_data')
async def update_user_data(
    user_data: UserModelUpdate= Depends(), 
    user: User = Depends(user_logic.get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    try:
        data = user_logic.update_user_data( user_data,user, session)
        return data
    except HTTPException:
        raise
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f'Integrity error: {str(e.orig)}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# remove account
@router.delete('/remove')
async def remove_account(
    user:Annotated[User,Depends(user_logic.get_current_user)],
    session:Session=Depends(get_db)
    ) ->dict:

    try:
        data = user_logic.remove_account(user,session)
        return data

    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"An error occurred: {str(e)}")
    


# update password

@router.patch('/update_password')
async def update_user_password(
    user:Annotated[User,Depends(user_logic.get_current_user)],
    data:UpdatePassword,
    session:Session=Depends(get_db),
    )->dict:

    try:
        user = user_logic.update_password(user,data,session)
        if not user :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid username or password',
                            headers={"WWW-Authenticate": "Bearer"})
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"An error occurred: {str(e)}")


