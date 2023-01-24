import unittest
import os

import requests

from tests.unit.test_data_mixin import TestDataMixin

from user_sound.core.postgres_repo import PostgresRepo

class IntegrationTests(unittest.TestCase, TestDataMixin):
    @classmethod
    def setUpClass(cls):
        cls.postgres_repo = PostgresRepo()

    def setUp(self) -> None:
        super().setUp()

        self.load_test_data()

        self.host = os.environ["HOST_URL"]
        self.user_base_url = f"{self.host}/v1/users"
        self.audio_base_url = f"{self.host}/v1/audio"


        self.create_user_payload = {
            "email": self.email,
            "name": self.name, 
            "address": self.address,
            "image":self.image
        }

        self.create_audio_payload = {
            "session_id": self.session_id,
            "step_count": self.step_count,
            "selected_tick": self.selected_tick,
            "ticks": self.ticks,
            "user_id": self.user_id
        }

    def tearDown(self) -> None:
        super().tearDown()
        # Cleans test user
        test_user = self.postgres_repo.get_user_by_email(self.email)
        if test_user is not None:
            self.postgres_repo.delete_user(test_user.id)
        test_audio = self.postgres_repo.get_audio_by_session_id_and_step_count(self.session_id, self.step_count)
        if test_audio is not None:
            self.postgres_repo.delete_audio(self.session_id, self.step_count)

    def test_create_user(self):
        # create user
        response = requests.post(url=f"{self.user_base_url}/", json=self.create_user_payload)
        self.assertEqual(200, response.status_code)
        created_user = self.postgres_repo.get_user_by_email(email=self.email)
        self.assertIsNotNone(created_user)
        # fails to create same user
        response = requests.post(url=f"{self.user_base_url}/", json=self.create_user_payload)
        self.assertEqual(400, response.status_code)

    def test_list_user(self):
        user = self._create_new_user()
        self.postgres_repo.create_user(user)
        response = requests.get(url=f"{self.user_base_url}/")
        self.assertEqual(200, response.status_code)


    def test_update_user(self):
        user = self._create_new_user()
        new_user = self.postgres_repo.create_user(user)
        update_payload = self.create_user_payload.copy()
        update_payload.update({ 
            "name":f"{self.name} The Second"
        })
        response = requests.put(url=f"{self.user_base_url}/{new_user.id}", json=update_payload)
        self.assertEqual(204, response.status_code)

    def test_delete_user(self):
        user = self._create_new_user()
        new_user = self.postgres_repo.create_user(user)
        response = requests.delete(url=f"{self.user_base_url}/{new_user.id}")
        self.assertEqual(204, response.status_code)

    def test_create_audio(self):
        user = self._create_new_user()
        new_user = self.postgres_repo.create_user(user)
        self.create_audio_payload.update({
            "user_id": new_user.id
        }) 
        # create audio
        response = requests.post(url=f"{self.audio_base_url}/", json=self.create_audio_payload)
        self.assertEqual(200, response.status_code)
        created_audio = self.postgres_repo.get_audio_by_session_id_and_step_count(self.session_id, self.step_count)
        self.assertIsNotNone(created_audio)
        # fails to create same audio
        response = requests.post(url=f"{self.audio_base_url}/", json=self.create_audio_payload)
        self.assertEqual(400, response.status_code)

    def test_list_audio(self):
        user = self._create_new_user()
        new_user = self.postgres_repo.create_user(user)
        audio = self._create_audio()
        audio.user_id = new_user.id
        self.postgres_repo.create_audio(audio)
        response = requests.get(url=f"{self.audio_base_url}/")
        self.assertEqual(200, response.status_code)

    def test_update_audio(self):
        user = self._create_new_user()
        new_user = self.postgres_repo.create_user(user)
        audio = self._create_audio()
        audio.user_id = new_user.id
        self.postgres_repo.create_audio(audio)
        update_payload = self.create_audio_payload.copy()
        update_payload.update({ 
            "selected_tick": self.selected_tick + 1,
            "user_id":new_user.id
        })
        response = requests.put(url=f"{self.audio_base_url}/", json=update_payload)
        self.assertEqual(204, response.status_code)

    def test_remove_audio(self):
        user = self._create_new_user()
        new_user = self.postgres_repo.create_user(user)
        audio = self._create_audio()
        audio.user_id = new_user.id
        self.postgres_repo.create_audio(audio)
        response = requests.delete(url=f"{self.audio_base_url}/{audio.session_id}")
        self.assertEqual(204, response.status_code)

