from pydantic import BaseModel


class RunSettings(BaseModel):
    host: str
    port: int
    app_title: str
    log_level: str

    @property
    def url(self):
        return f"http://{self.host}"
