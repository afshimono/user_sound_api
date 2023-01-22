import json
import unittest

from fastapi import Request
from fastapi.testclient import TestClient

from user_sound.core.service import Service
from tests.unit.db_mock import MockRepo
from user_sound.main import app
from user_sound.v1.users import get_user_service
from user_sound.v1.audio import get_audio_service
from tests.unit.test_service import TestBaseService


class TestBaseEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = MockRepo()
        self.service = Service(repo=self.repo)
        self.client = TestClient(app)
        app.dependency_overrides[get_user_service] = self.override_get_service
        app.dependency_overrides[get_audio_service] = self.override_get_service

    def override_get_service(self):
        return self.service


class TestEndpoints(TestBaseEndpoint, TestBaseService):
    def setUp(self) -> None:
        TestBaseEndpoint.setUp(self)
        TestBaseService.setUp(self)

    def test_user_list(self):
        self._add_default_user()
        response = self.client.get("/v1/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_user_list_filter(self):
        self._add_default_user()
        user2 = self._create_user()
        user2.id = 2
        user2.email = "new_"+self.email
        self.repo.users[2] = user2
        response = self.client.get(f"/v1/users?email={self.email}")
        self.assertEqual(200, response.status_code)
        response_payload = response.json()
        self.assertEqual(1, len(response_payload["data"]))
        self.assertEqual(self.email, response_payload["data"][0]["attributes"]["email"])


    def test_user_create(self):
        payload = {
            "email": f'new_{self.email}',
            "name": self.name, 
            "address": self.address,
            "image":self.image
        }
        response = self.client.post("/v1/users/", json=payload)
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/v1/users/", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_user_update(self):
        self._add_default_user()
        payload = {
            "email": "test2@test.com",
            "address": self.name,
            "name": self.name,
            "image": self.image
        }
        response = self.client.put("/v1/users/1", json=payload)
        self.assertEqual(response.status_code, 204)

    def test_user_delete(self):
        self._add_default_user()
        response = self.client.delete("/v1/users/1")
        self.assertEqual(response.status_code, 204)

    def test_audio_create(self):
        self._add_default_user()
        payload = {
            "session_id": self.session_id,
            "step_count": self.step_count,
            "selected_tick": self.selected_tick,
            "ticks": self.ticks,
            "user_id": self.user_id
        }
        response = self.client.post("/v1/audio/", json=payload)
        self.assertEqual(response.status_code, 200)

    def test_audio_update(self):
        self._add_default_user()
        self._add_default_audio()
        payload = {
            "session_id": self.session_id,
            "step_count": self.step_count,
            "selected_tick": self.selected_tick+1,
            "ticks": self.ticks,
            "user_id": self.user_id
        }
        response = self.client.put("/v1/audio/", json=payload)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.repo.audios[f"{self.session_id}_{self.step_count}"].selected_tick, self.selected_tick+1)

    def test_audio_list(self):
        self._add_default_user()
        self._add_default_audio()
        response = self.client.get("/v1/audio/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_audio_list_by_session_id(self):
        self._add_default_user()
        self._add_default_audio()
        response = self.client.get("/v1/audio/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_audio_delete(self):
        self._add_default_user()
        self._add_default_audio()
        response = self.client.delete("/v1/audio/1")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, len(self.repo.audios))