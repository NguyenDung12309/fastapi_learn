from pydantic import BaseModel


class CreateOrGetAuthorSchema(BaseModel):
    name: str
