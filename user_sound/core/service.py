from typing import Optional

from user_sound.core.schemas import (
    UserBase, 
    UserWithId,
    SingleUserDTO,
    MultipleUserDTO,
    Metadata,
    Audio,
    SingleAudioDTO,
    MultipleAudioDTO)
from user_sound.core.models import UserModel, AudioModel
from user_sound.core.exceptions import InsertError, NotFound
from user_sound.core.repository import Repo



class Service:
    def __init__(self, repo: Repo) -> None:
        self.repo = repo

    def list_users(self,
                    name:Optional[str] = None,
                    email:Optional[str] = None,
                    address:Optional[str] = None) -> MultipleUserDTO:
        user_list = self.repo.list_users(name=name, email=email, address=address)
        single_response_list = [self._make_single_user_response(user) for user in user_list]
        return MultipleUserDTO(data=single_response_list)

    def get_user_by_email(self, email: str) -> UserModel:
        return self.repo.get_user_by_email(email)

    def get_user_by_id(self, user_id: int) -> UserModel:
        user_entity = self.repo.get_user_by_id(user_id)
        if not user_entity:
            raise NotFound(f"User does not exist for id {user_id}")
        return self._make_single_user_response(user_entity)

    def create_user(self, user: UserBase) -> UserModel:
        new_user = user.as_user_model()
        user_entity = self.repo.create_user(user=new_user)
        return self._make_single_user_response(user_entity)

    def update_user(self, user: UserWithId) -> None:
        self.repo.update_user(user)

    def delete_user(self, user_id: int) -> None:
        try:
            self.repo.delete_user(user_id)
        except NotFound as e:
            raise NotFound(e) from e

    def create_audio(self, audio: Audio) -> Audio:
        """
        existing_audio = self.repo.get_audio_by_session_id_and_step_count(session_id=audio.session_id, step_count=audio.step_count)
        if existing_audio is not None:
            raise InsertError(f"Audio already exists for the session {audio.session_id} and step {audio.step_count}.")
        """
        new_audio = audio.as_audio_model()
        audio_entity = self.repo.create_audio(audio=new_audio)
        return self._make_single_audio_response(audio_entity)

    def list_audio(self, session_id:Optional[int] = None) -> MultipleAudioDTO:
        audio_list = self.repo.list_audio(session_id)
        single_response_list = [self._make_single_audio_response(audio) for audio in audio_list]
        return MultipleAudioDTO(data=single_response_list)

    def delete_audio(self, session_id: int, step_count:Optional[int] = None) -> None:
        try:
            self.repo.delete_audio(session_id=session_id, step_count=step_count)
        except NotFound as e:
            raise NotFound(e) from e

    def update_audio(self, audio: Audio) -> None:
        try:
            self.repo.update_audio(audio)
        except NotFound as e:
            raise NotFound(e) from e

    def _make_single_user_response(self, user:UserModel) -> SingleUserDTO:
        user_data = UserWithId.from_user_model(user)
        metadata = Metadata.from_model(user)
        return SingleUserDTO(attributes=user_data, metadata=metadata)

    def _make_single_audio_response(self, audio: Audio) -> SingleAudioDTO:
        audio_data = Audio.from_audio_model(audio)
        metadata = Metadata.from_model(audio)
        return SingleAudioDTO(attributes=audio_data, metadata=metadata)

