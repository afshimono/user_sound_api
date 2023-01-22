import email
from typing import List, Optional

from user_sound.core.repository import Repo
from user_sound.core.models import UserModel, AudioModel
from user_sound.core.exceptions import NotFound, InsertError
from user_sound.core.schemas import (UserWithId, Audio)


class MockRepo(Repo):
    def __init__(self) -> None:  # sourcery skip: dict-literal
        self.users = dict()
        self.audios = dict()

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        user_list = [user for user in list(self.users.values())
                     if user.email == email]
        return user_list[0] if user_list else None

    def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        return self.users.get(user_id)

    def create_user(self, user: UserModel) -> UserModel:
        if self.get_user_by_email(user.email) is not None:
            raise InsertError("User already exists.")
        id = len(self.users.keys()) + 1
        user.id = id
        self.users[id] = user
        return user

    def update_user(self, user: UserWithId) -> None:
        if user.id not in self.users:
            raise NotFound("User not found.")

        existing_user = self.users[user.id]

        existing_user.email = user.email
        existing_user.address = user.address
        existing_user.name = user.name

        self.users[user.id] = existing_user

    def delete_user(self, user_id: int) -> None:
        del self.users[user_id]

    def list_users(self, 
            name:Optional[str]=None, 
            email:Optional[str]=None, 
            address:Optional[str]=None) -> List[UserModel]:
        all_users = self.users.values()
        if email:
            all_users = [user for user in all_users if user.email == email]
        if name:
            all_users = [user for user in all_users if name in user.name]
        if address:
            all_users = [user for user in all_users if address in user.address]
        return all_users

    def get_audio_by_session_id_and_step_count(self, session_id: int, step_count: int) -> Optional[AudioModel]:
        return self.audios.get(f"{session_id}_{step_count}")

    def create_audio(self, audio: Audio) -> Audio:
        self.audios[self._make_audio_key(audio)] = audio
        return audio

    def update_audio(self, audio: Audio) -> None:
        if self._make_audio_key(audio) not in self.audios:
            raise NotFound("Audio not found.")
        self.audios[self._make_audio_key(audio)] = audio

    def list_audio(self, session_id: Optional[int] = None) -> List[AudioModel]:
        return (
            [
                audio
                for audio in list(self.audios.values())
                if audio.session_id == session_id
            ]
            if session_id
            else list(self.audios.values())
        )

    def delete_audio(self, session_id: int, step_count: Optional[int] = None) -> None:
        if step_count:
            del self.audios[f"{session_id}_{step_count}"]
        else:
            audio_key_list = [key for key in self.audios.keys() if key.startswith(f"{session_id}_")]
            for key in audio_key_list:
                del self.audios[key]

    def _make_audio_key(self, audio:Audio) -> str:
        return f"{audio.session_id}_{audio.step_count}"
