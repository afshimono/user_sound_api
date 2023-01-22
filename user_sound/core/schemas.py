import datetime as dt
from typing import List, Optional

from pydantic import BaseModel, EmailStr, HttpUrl,parse_obj_as, validator

from user_sound.core.models import UserModel, AudioModel

class Metadata(BaseModel):
    created_at: Optional[dt.datetime]=None
    updated_at: Optional[dt.datetime]=None

    @classmethod
    def from_model(cls, model: BaseModel) -> 'Metadata':
        return Metadata(
            created_at=model.created_at,
            updated_at=model.updated_at
        )


class UserBase(BaseModel):
    email: EmailStr
    name: str
    address: str
    image: HttpUrl

    def as_user_model(self):
        return (
            UserModel(
                email=self.email,
                name=self.name,
                address=self.address,
                image=str(self.image)
            )
        )


    @classmethod
    def from_user_model(cls, user_model: UserModel) -> 'UserBase':
        return UserBase(
            email=user_model.email,
            address=user_model.address,
            name=user_model.name,
            image=parse_obj_as(HttpUrl,user_model.image)
        )


class UserWithId(UserBase):
    id: int

    def as_user_model(self):
        user_model = super().as_user_model()
        user_model.id = self.id
        return user_model

    @classmethod
    def from_user_model(cls, user_model: UserModel) -> 'UserWithId':
        base_user_dict = super().from_user_model(user_model).dict()
        user_schema = UserWithId(id=user_model.id,**base_user_dict)
        return user_schema

class SingleUserDTO(BaseModel):

    attributes: UserWithId
    metadata: Metadata

class MultipleUserDTO(BaseModel):

    data: List[SingleUserDTO]

class Audio(BaseModel):
    session_id: int
    step_count: int
    user_id: int
    selected_tick: int
    ticks: List[int]

    @validator('step_count')
    def step_count_range(cls,v):
        if v not in range(10):
            raise ValueError("step_count must be between 0 and 9.")
        return v

    @validator('selected_tick')
    def selected_tick_range(cls, v):
        if v not in range(15):
            raise ValueError("selected_tick must be between 0 and 14.")
        return v

    @validator('ticks')
    def ticks_size_and_values(cls, v):
        if len(v) != 15:
            raise ValueError("ticks must have 15 elements.")
        if min(v) < -100:
            raise ValueError("ticks values must not be smaller than -100.")
        if max(v) > -10:
            raise ValueError("ticks values must not be larger than -10.")
        return v

    def as_audio_model(self):
        return (
            AudioModel(
                session_id=self.session_id,
                step_count=self.step_count,
                user_id=self.user_id,
                selected_tick=self.selected_tick,
                ticks=self.ticks
            )
        )

    @classmethod
    def from_audio_model(cls, audio_model: AudioModel) -> 'Audio':
        return Audio(
            session_id=audio_model.session_id,
            step_count=audio_model.step_count,
            selected_tick=audio_model.selected_tick,
            user_id=audio_model.user_id,
            ticks=audio_model.ticks
        )

class SingleAudioDTO(BaseModel):
    attributes: Audio
    metadata: Metadata

class MultipleAudioDTO(BaseModel):
    data: List[SingleAudioDTO]