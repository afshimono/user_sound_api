import unittest

from tests.unit.test_data_mixin import TestDataMixin
from user_sound.core.schemas import UserWithId, Audio, UserBase
from user_sound.core.models import UserModel, AudioModel
from user_sound.core.service import Service
from tests.unit.db_mock import MockRepo
from user_sound.core.exceptions import NotFound

class TestBaseService(unittest.TestCase, TestDataMixin):
    def setUp(self) -> None:

        self.repo = MockRepo()
        self.service = Service(repo=self.repo)

        self.load_test_data()

    def _add_default_user(self):
        self.repo.users[1] = self.default_user

    def _add_default_audio(self):
        self.repo.audios[f"{self.session_id}_{self.step_count}"] = self.default_audio

class TestService(TestBaseService):

    def setUp(self) -> None:
        super().setUp()

    def test_list_users(self):
        user1_dto = self.service.create_user(self.user_create)
        user1 = user1_dto.attributes
        self.user_create.email = 'test2@test.com'
        user2_dto = self.service.create_user(self.user_create)
        user2 = user2_dto.attributes
        multiple_user_dto = self.service.list_users()
        user_list = [user.attributes for user in multiple_user_dto.data]
        email_list = [user.email for user in user_list]
        self.assertIn(user1.email, email_list)
        self.assertIn(user2.email, email_list)

    def test_get_user_by_email(self):
        self._add_default_user()
        user = self.service.get_user_by_email(self.email)
        self.assertEqual(self.email, user.email)

    def test_create_user(self):
        user_dto = self.service.create_user(self.user_create)
        user = user_dto.attributes
        db_user = self.repo.users[1]
        self.assertEqual(user.email, db_user.email)

    def test_update_user(self):
        self._add_default_user()
        user_update = UserWithId(
            email="test2@email.com",
            name=self.name,
            address=self.address,
            image=self.image,
            id=self.user_id
        )
        self.service.update_user(user_update)
        self.assertEqual("test2@email.com",self.default_user.email)
        with self.assertRaises(NotFound) as context:
            user_update.id = 5
            self.service.update_user(user_update)

    def test_delete_user(self):
        self.repo.users[1] = UserModel(email=self.email, id=1)
        self.service.delete_user(1)
        self.assertEqual(len(self.repo.users), 0)

    def test_list_audio_by_session_id(self):
        self._add_default_user()
        self.repo.audios[f"{self.session_id}_{self.step_count}"] = self.default_audio
        audio_2 = self._create_audio()
        audio_2.step_count = 2
        self.repo.audios[f"{self.session_id}_2"] = audio_2
        audio_3 = self._create_audio()
        audio_3.session_id = 2
        self.repo.audios["2_1"] = audio_3
        audio_dto = self.service.list_audio(session_id=self.session_id)
        audio_dto_list = audio_dto.data
        session_ids = set([audio.attributes.session_id for audio in audio_dto_list])
        self.assertEqual(1,len(session_ids))
        self.assertEqual(self.session_id, session_ids.pop())

    def test_list_audio(self):
        self._add_default_user()
        self.repo.audios[f"{self.session_id}_{self.step_count}"] = self.default_audio
        audio_dto_list = self.service.list_audio(session_id=1)
        audio_list = audio_dto_list.data
        self.assertEqual(len(audio_list), 1)

    def test_create_audio(self):
        self._add_default_user()
        audio_create = Audio(
            session_id=self.session_id,
            step_count=self.step_count,
            selected_tick=self.selected_tick,
            ticks=self.ticks,
            user_id=self.user_id
        )
        single_audio_dto_created = self.service.create_audio(audio_create)
        audio_created = single_audio_dto_created.attributes
        self.assertEqual(audio_create.session_id, audio_created.session_id)
        self.assertEqual(audio_create.step_count, audio_created.step_count)
        self.assertEqual(audio_create.selected_tick, audio_created.selected_tick)
        self.assertEqual(audio_create.ticks, audio_created.ticks)

    def test_update_audio(self):
        self._add_default_user()
        self._add_default_audio()
        audio_update = Audio(
            session_id=self.session_id,
            step_count=self.step_count,
            selected_tick=self.selected_tick+3,
            ticks=self.ticks,
            user_id=self.user_id
        )
        self.service.update_audio(audio_update)
        self.assertEqual(self.repo.audios[f"{self.session_id}_{self.step_count}"].selected_tick, self.selected_tick+3)

    def test_delete_audio(self):
        self._add_default_user()
        self._add_default_audio()
        self.service.delete_audio(session_id=self.session_id, step_count=self.step_count)
        self.assertEqual(len(self.repo.audios), 0)