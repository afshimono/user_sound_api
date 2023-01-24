from typing import List, Optional
import datetime as dt
import os

import urllib.parse
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.exc import  IntegrityError

from user_sound.core.models import UserModel, AudioModel
from user_sound.core.schemas import  UserWithId, Audio
from user_sound.settings import env_vars
from user_sound.core.exceptions import NotFound, InsertError
from user_sound.core.repository import Repo
    

class PostgresRepo(Repo):

    def __init__(self) -> None:
        if os.environ.get("ENV") == "debug":
            url_str = f"postgresql://{urllib.parse.quote_plus(env_vars.db_login)}:{urllib.parse.quote_plus(env_vars.db_password)}"\
                    + f"@{env_vars.db_url}/{env_vars.db_name}"
        elif os.environ.get("ENV") == "gcloud":
            url_str = sqlalchemy.engine.url.URL.create(
                drivername="postgresql+pg8000",
                username=env_vars.db_login,
                password=env_vars.db_password,
                database=env_vars.db_name,
                query={
                    "unix_sock": f"{env_vars.instance_unix_socket}/.s.PGSQL.5432"
                },
            )
        engine = create_engine(url_str)
        self.session = sessionmaker(
            autocommit=False, autoflush=False, bind=engine)

    def list_users(self,
                    name:Optional[str] = None,
                    email:Optional[str] = None,
                    address:Optional[str] = None) -> List[UserModel]:
        with self.session() as db:
            filter_list = []
            if name:
                filter_list.append(UserModel.name.ilike(f"%{name}%"))
            if email:
                filter_list.append(UserModel.email == email)
            if address:
                filter_list.append(UserModel.address.ilike(f"%{address}%"))
            user_query =  db.query(UserModel).filter(*filter_list)
            return user_query.all()

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        with self.session() as db:
            return db.query(UserModel).filter(UserModel.email == email).first()

    def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        with self.session() as db:
            return db.query(UserModel).filter(UserModel.id == user_id).first()

    def create_user(self, user: UserModel) -> UserModel:
        with self.session() as db:
            user.created_at = dt.datetime.now()
            user.updated_at = dt.datetime.now()
            try:
                db.add(user)
                return self._commit_and_return_refreshed(db, user)
            except IntegrityError as e:
                raise InsertError(f"User already exists for email {user.email}.") from e

    def update_user(self, user: UserWithId) -> None:
        with self.session() as db:
            existing_user = db.query(UserModel).filter(UserModel.id == user.id).first()
            if existing_user is None:
                raise NotFound("User not found.")
            existing_user.email = user.email
            existing_user.name = user.name
            existing_user.address = user.address
            existing_user.image = str(user.image)
            existing_user.updated_at = dt.datetime.now()

            db.commit()

    def delete_user(self, user_id: int) -> None:
        with self.session() as db:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if user is None:
                raise NotFound("User was not found in DB.")
            self._delete_and_commit(db, user)


    def get_audio_by_session_id_and_step_count(self, session_id: int, step_count: int) -> Optional[AudioModel]:
        with self.session() as db:
            return db.query(AudioModel) \
                .filter(AudioModel.session_id == session_id) \
                .filter(AudioModel.step_count == step_count) \
                .first()
    
    def list_audio(self, session_id: Optional[int] = None) -> List[AudioModel]:
        if session_id is None:
            with self.session() as db:
                return db.query(AudioModel).all()
        else:
            with self.session() as db:
                return db.query(AudioModel) \
                    .filter(AudioModel.session_id == session_id) \
                    .all()

    def create_audio(self, audio: Audio) -> Audio:
        with self.session() as db:
            user = db.query(UserModel).filter(UserModel.id == audio.user_id).first()
            if user is None:
                raise NotFound("User was not found in DB.")
            audio.created_at = dt.datetime.now()
            audio.updated_at = dt.datetime.now()
            try:
                db.add(audio)
                return self._commit_and_return_refreshed(db, audio)
            except IntegrityError as e:
                raise InsertError("Session Id / Step Count entry already exists.") from e
    
    def update_audio(self, audio: Audio) -> None:
        with self.session() as db:
            existing_audio = db.query(AudioModel) \
                .filter(AudioModel.session_id == audio.session_id) \
                .filter(AudioModel.step_count == audio.step_count) \
                .first()
            if not existing_audio:
                raise NotFound(f"No audio exists for session id {audio.session_id} and step count {audio.step_count}") 
            existing_audio.selected_tick = audio.selected_tick
            existing_audio.ticks = audio.ticks
            existing_audio.user_id = audio.user_id
            existing_audio.updated_at = dt.datetime.now()
            db.commit()


    def delete_audio(self, session_id: int, step_count: Optional[int] = None) -> None:
        with self.session() as db:
            delete_query = db.query(AudioModel).filter(AudioModel.session_id == session_id)
            if step_count is not None:
                delete_query = delete_query.filter(AudioModel.step_count == step_count)
            delete_query.delete()
            db.commit()
    

    def _commit_and_return_refreshed(self, db, arg1):
        db.commit()
        db.refresh(arg1)
        return arg1

    def _delete_and_commit(self, db, arg) -> None:
        db.delete(arg)
        db.commit()


postgres_repo = PostgresRepo()