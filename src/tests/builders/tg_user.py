from faker import Faker


class FakeTgUser:
    fake: Faker = Faker()

    def __init__(self) -> None:
        self.tg_id: int = self.fake.random_int(111111111, 999999999, 123)
        self.password: str = self.fake.password()
        self.user_email: str = self.fake.email()

    def get_data(self) -> dict[str, str | int]:
        return {
            "tg_id": self.tg_id,
            "password": self.password,
            "user_email": self.user_email,
        }
