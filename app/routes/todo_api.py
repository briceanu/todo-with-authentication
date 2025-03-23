from fastapi import APIRouter, Depends, status, HTTPException,Body, Query
from sqlalchemy.orm import Session
from db.db_connection import get_db
import routes.user_logic as user_logic
from typing import Annotated
from models import User
from . import todo_logic
from sqlalchemy.exc import IntegrityError
from schemas import TodoModelCreate, TodoModelUpdate, TodoModelResponse
import uuid
from datetime import date
import re
router = APIRouter(prefix='/todo',tags=['all the routes for the todo'])


@router.post('/create')
async def create_a_todo(
    user:Annotated[User,Depends(user_logic.get_current_user)],
    todo_data:Annotated[TodoModelCreate,Body()],
    session:Session=Depends(get_db),
    ):
    try:
        todo = todo_logic.create_todo(user,todo_data,session)
        return todo

    except HTTPException:
        raise 
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'an error occured {str(e.orig)}')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'an error occured: {str(e)}')
    

@router.get('/all')
async def list_all_todos(

    session:Session=Depends(get_db),
    ):
    try:
        todo = todo_logic.list_all_todos(session)
        return todo

 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'an error occured: {str(e)}')
    




@router.get('/user_todos')
async def list_todos(
    user:User=Depends(user_logic.get_current_user),
    session:Session=Depends(get_db),
    ):
    try:
        todo = todo_logic.list_todos_belonging_to_user(user,session)
        return todo

 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'an error occured: {str(e)}')
    




@router.put('/update')
async def update_a_todo(
    user:Annotated[User,Depends(user_logic.get_current_user)],
    todo_id:uuid.UUID,
    todo_data:Annotated[TodoModelUpdate,Body()],
    session:Session=Depends(get_db),
    ):
    try:
        todo = todo_logic.update_todo(user,todo_id,todo_data,session)
        return todo

    except HTTPException:
        raise 
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'an error occured {str(e.orig)}')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'an error occured: {str(e)}')
    


@router.delete('/remove')
async def remove_a_todo(
    user:Annotated[User,Depends(user_logic.get_current_user)],
    todo_id:Annotated[uuid.UUID,Body()],
    session:Session=Depends(get_db),
    ):
    try:
        todo = todo_logic.remove_todo(user,todo_id,session)
        return todo

    except HTTPException:
        raise 
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'an error occured {str(e.orig)}')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'an error occured: {str(e)}')
    



"""API's for filtering data"""

@router.get('/title')
async def get_todos_by_title(
                    search:Annotated[str,Query()],
                    completed:Annotated[bool,Query()],
                    session:Session=Depends(get_db),

                    ) -> list[TodoModelResponse]:
    try:
        todo = todo_logic.get_todo_by_title_search(search,completed,session)
        return todo
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'an error occured: {str(e)}')
    

@router.get('/year')
async def get_todos_by_year(
                    year:str = Query(),
                    session:Session = Depends(get_db),

                    ) -> list[TodoModelResponse]:
    try:
        if not re.fullmatch(r"\d{4}", year):  # Ensures only 4-digit years are allowed
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Year must be a valid 4-digit number (e.g., 2023)"
            )
        valid_year = int(year)
        todo = todo_logic.get_todos_by_year(valid_year,session)

        return todo
    except HTTPException:
        raise 

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'an error occured: {str(e)}')
    