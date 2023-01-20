from abc import ABC, abstractmethod
from typing import Optional, List

from user_sound.core.models import UserModel, AudioModel
from user_sound.core.schemas import UserBase, UserWithId

class Repo(ABC):

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        pass

    @abstractmethod
    def list_users(self,
                    name:Optional[str]=None,
                    email:Optional[str]=None,
                    address:Optional[str]=None) -> List[UserModel]:
        pass

    @abstractmethod
    def create_user(self, user: UserBase) -> UserModel:
        pass

    @abstractmethod
    def update_user(self, user: UserWithId) -> None:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    def get_audio_by_session_id_and_step_count(self, session_id: int, step_count: int) -> Optional[AudioModel]:
        pass

    @abstractmethod
    def list_audio(self) -> List[AudioModel]:
        pass

    @abstractmethod
    def create_audio(self, audio: AudioModel) -> AudioModel:
        pass

    @abstractmethod
    def update_audio(self, audio: AudioModel) -> None:
        pass

    @abstractmethod
    def delete_audio(self, session_id: int, step_count: Optional[int] = None) -> None:
        pass