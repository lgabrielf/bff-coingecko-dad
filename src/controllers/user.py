from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.user_model import UserModel
from src.schemas.user import UserCreateDTO, UserSchemaUp, UserDTO

from src.services.user_service import get_session, get_current_user
from src.config.security import generate_hash_password
from src.config.auth import authenticate, criar_token_acesso

router = APIRouter()

# GET Logado
@router.get('/logado', response_model=UserDTO)
def get_logado(logged_user: UserModel = Depends(get_current_user)):
    return logged_user

# POST / SignUP
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserDTO)
async def post_user(user: UserCreateDTO, db: AsyncSession = Depends(get_session)):
    # Ignore any role information from the input, only allow name and password
    async with db as session:
        query = select(UserModel).filter(UserModel.name == user.name)
        result = await session.execute(query)
        existing_user = result.scalars().first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already in use."
            )

    # Ensure role is not set from the input
    new_user: UserModel = UserModel(
        name=user.name,
        password=generate_hash_password(user.password)
    )
    async with db as session:
        try:
            session.add(new_user)
            await session.commit()
            return new_user
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating user."
            )

@router.get('/', response_model=List[UserDTO])
async def get_users(db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserDTO] = result.scalars().unique().all()

        return users

@router.get('/{user_id}', response_model=UserDTO, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserDTO = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(detail='User no found', status_code=status.HTTP_404_NOT_FOUND)

# PUT user
@router.put('/{user_id}', response_model=UserDTO, status_code=status.HTTP_202_ACCEPTED)
async def put_user(
    user_id: int,
    user: UserSchemaUp,
    db: AsyncSession = Depends(get_session),
    logged_user: UserModel = Depends(get_current_user)
):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_up: UserModel = result.scalars().unique().one_or_none()

        if user_up:
            if getattr(logged_user, "role", None) != "admin" and logged_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only edit your own user."
                )

            if user.name:
                user_up.name = user.name
            if user.password:
                user_up.password = generate_hash_password(user.password)

            if getattr(logged_user, "role", None) == "admin" and user.role is not None:
                user_up.role = user.role

            await session.commit()
            return user_up
        else:
            raise HTTPException(detail='User no found', status_code=status.HTTP_404_NOT_FOUND)

# DELETE user
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_session),
    logged_user: UserModel = Depends(get_current_user)
):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_del: UserModel = result.scalars().unique().one_or_none()

        if user_del:
            if getattr(logged_user, "role", None) != "admin" and logged_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only delete your own user."
                )

            await session.delete(user_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='User no found', status_code=status.HTTP_404_NOT_FOUND)

# POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate(name=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect access data.')
        
    return JSONResponse(content={"access_token": criar_token_acesso(sub=user), "token_type": "bearer"}, status_code=status.HTTP_200_OK)