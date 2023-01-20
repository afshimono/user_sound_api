from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from user_sound.core.exceptions import  NotFound, InsertError
from user_sound.core.schemas import Audio
from user_sound.core.service import Service
from user_sound.core.postgres_repo import postgres_repo

service = Service(repo=postgres_repo)


def get_audio_service() -> Service:
    return service


router = APIRouter(prefix="/v1/audio",
                   tags=["audio"],
                   responses={
                       404: {
                           "description": "Not found"
                       }
                   })


@router.post("/")
async def create_audio(audio: Audio,  service: Service = Depends(get_audio_service)):

    try:
        return service.create_audio(audio)
    except InsertError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("/")
async def list_audio( service: Service = Depends(get_audio_service)):
    return service.list_audio()

@router.get("/{session_id}")
async def list_audio_by_session_id(session_id: int, service: Service = Depends(get_audio_service)):
    return service.list_audio(session_id=session_id)


@router.put("/")
async def update_audio(audio: Audio,  service: Service = Depends(get_audio_service)):
    try:
        service.update_audio(audio=audio)
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{session_id}")
async def delete_audio(session_id: int, step_count:Optional[int] = None, service: Service = Depends(get_audio_service)):
    service.delete_audio(session_id=session_id, step_count=step_count)
    return Response(status_code=status.HTTP_204_NO_CONTENT)