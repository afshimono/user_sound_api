from user_sound.core.models import UserModel, AudioModel
from user_sound.core.schemas import UserBase

class TestDataMixin:

    def load_test_data(self) -> None:
        # user const
        self.email = 'test@test.com'
        self.name = 'John Doe'
        self.address = 'Test Street'
        self.image = 'http://test.com/image.jpg'
        self.user_id = 1
        self.user_create = UserBase(
            email=self.email,
            name=self.name,
            address=self.address,
            image=self.image
        )

        self.default_user = UserModel(
            email=self.email,
            name=self.name,
            address=self.address,
            image=self.image,
            id=self.user_id
        )

        # audio const
        self.session_id = 1
        self.step_count = 1
        self.selected_tick = 1
        self.ticks = [-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24]
        self.default_audio = AudioModel(
            session_id=self.session_id,
            step_count=self.step_count,
            selected_tick=self.selected_tick,
            ticks=self.ticks,
            user_id=self.user_id
        )

    def _create_audio(self):
        return AudioModel(
            session_id=self.session_id,
            step_count=self.step_count,
            selected_tick=self.selected_tick,
            ticks=self.ticks,
            user_id=self.user_id
        )

    def _create_user(self):
        return UserModel(
            email=self.email,
            name=self.name,
            address=self.address,
            image=self.image,
            id=self.user_id
        )

    def _create_new_user(self):
        return UserModel(
            email=self.email,
            name=self.name,
            address=self.address,
            image=self.image
        )