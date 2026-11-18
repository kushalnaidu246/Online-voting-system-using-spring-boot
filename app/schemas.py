"""Request/response shapes. JSON uses camelCase (userId, candidateId) like the
original Spring API."""
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=True
    )


class UserCreate(CamelModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)


class UserOut(CamelModel):
    id: int
    username: str


class CandidateCreate(CamelModel):
    name: str = Field(max_length=100)

    @field_validator("name")
    @classmethod
    def not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name must not be blank")
        return v


class CandidateOut(CamelModel):
    id: int
    name: str


class VoteOut(CamelModel):
    id: int
    user_id: int
    candidate_id: int


class ResultOut(CamelModel):
    candidate_id: int
    name: str
    votes: int
