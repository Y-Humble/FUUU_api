from faker import Faker


class FakeMeme:
    fake: Faker = Faker()

    def __init__(self) -> None:
        self.top_text: str = self.fake.word()
        self.bottom_text: str = self.fake.word()

    def get_text(self) -> dict[str, str]:
        return {"top_text": self.top_text, "bottom_text": self.bottom_text}
