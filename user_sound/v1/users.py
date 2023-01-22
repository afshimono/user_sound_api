from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from user_sound.core.exceptions import  NotFound, InsertError
from user_sound.core.schemas import UserBase, UserWithId
from user_sound.core.service import Service
from user_sound.core.postgres_repo import postgres_repo

service = Service(repo=postgres_repo)


def get_user_service() -> Service:
    return service


router = APIRouter(prefix="/v1/users",
                   tags=["users"],
                   responses={
                       404: {
                           "description": "Not found"
                       }
                   })


@router.post("/")
async def create_user(user: UserBase,  user_service: Service = Depends(get_user_service)):

    try:
        return user_service.create_user(user)
    except InsertError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("/")
async def list_users(name:Optional[str]=None, email:Optional[str]=None, address:Optional[str]=None, user_service: Service = Depends(get_user_service)):
    return user_service.list_users(name=name, email=email, address=address)

@router.get("/{user_id}")
async def get_user(user_id: int, user_service: Service = Depends(get_user_service)):
    try:
        return user_service.get_user_by_id(user_id)
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.put("/{user_id}")
async def update_user(user_id: int, user: UserBase,  user_service: Service = Depends(get_user_service)):
    user_to_be_updated = UserWithId(id=user_id, **user.dict())
    
    try:
        user_service.update_user(user_to_be_updated)
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{user_id}")
async def delete_user(user_id: int,  user_service: Service = Depends(get_user_service)):

    try:
        user_service.delete_user(user_id=user_id)
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    return Response(status_code=status.HTTP_204_NO_CONTENT)