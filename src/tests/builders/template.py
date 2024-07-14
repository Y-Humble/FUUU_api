from faker import Faker
from pathlib import Path

class FakeTemplate:
    fake: Faker = Faker()
    def __init__(self, template_name: str) -> None:
        self.title: str = template_name
        self.category: str = template_name.split("-")[0]

    def get_form_data(self):
        return {"title": self.title, "category": self.category}

    def new_form_data(self):
        template_name: str = "-".join(self.fake.name().split())
        return type(self)(template_name)

    def get_files_data(self, path: Path):
        image_path: Path = path / self.title
        return {"image": image_path.open("rb")}
