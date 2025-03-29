from sqlalchemy.orm import Session
from sqlalchemy import insert,select, and_, update, extract
from models import User, Todo
from schemas import TodoModelCreate, TodoModelUpdate
from fastapi.exceptions import HTTPException
from fastapi import status
import uuid
 


def create_todo(
        user:User,
        todo_data:TodoModelCreate,
        session:Session,
        ):

    user = session.execute(select(User).where(User.username==user)).scalar()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'no user with the username {user} found')

    stmt = insert(Todo).values(
        **todo_data.model_dump(),
        user_id=user.user_id
        )
    session.execute(stmt)
    session.commit()
    return {'success':'todo saved'}





# logic for listing all the todos
def list_all_todos(
                   page:int,
                   number_of_items:int,
                   session:Session,):
    offset = (page - 1) * number_of_items  # Correct calculation for pagination
    stmt = select(Todo).limit(number_of_items).offset(offset)
    todos = session.execute(stmt).scalars().all()
    return todos




def list_todos_belonging_to_user(user:User,session:Session):
    stmt = (select(Todo)
            .join(User,User.user_id==Todo.user_id)
            .where(User.username==user))
 
    todos = session.execute(stmt).scalars().all()
    return todos

 





def update_todo(req_user:User,
                todo_id:uuid.UUID,
                todo_data:TodoModelUpdate,
                session:Session,
                ):
    db_user = session.execute(select(User).where(User.username==req_user)).scalar_one_or_none()                
    if not db_user :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    stmt = (update(Todo)
            .where(and_(Todo.todo_id == todo_id, Todo.user_id == db_user.user_id)) 
            .values(**todo_data.model_dump())
            )

    result = session.execute(stmt)
    if result.rowcount == 0 :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this blog")
    session.commit()
    return {'success':'todo updated'}


 


def remove_todo(user:User,
                todo_id:uuid.UUID,
                session:Session,
                ):
    blog_user = session.execute(select(User).where(User.username==user)).scalar_one_or_none()
    if not user :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    todo = (session.execute(select(Todo)
                .where(Todo.todo_id == todo_id, Todo.user_id == blog_user.user_id))
                .scalar_one_or_none())

    if not todo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to remove this blog")

    session.delete(todo)
    session.commit()
    return {"success":"todo removed"}





#  learning how to filter data


# get todos that have in the title containts the word 'search'
def get_todo_by_title_search(search:str,completed:bool,session:Session):
    stmt = (select(Todo)
            .where(
                and_(Todo.title.ilike(f'%{search}%')
                    ,Todo.completed==completed)))
    data = session.execute(stmt).scalars().all()

    return data



# get todos by year
def get_todos_by_year(year:int,session:Session):
    stmt = select(Todo).where(extract('year', Todo.created_at) == year)
    data = session.execute(stmt).scalars().all()

    return data
 