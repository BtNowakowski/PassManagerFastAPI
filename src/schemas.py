import pydantic as _pydantic
from typing import List


class _PasswordBase(_pydantic.BaseModel):
    name: str


class PasswordCreate(_PasswordBase):
    length: int


class PasswordUpdate(_PasswordBase):
    value: str


class Password(_PasswordBase):
    id: int
    value: str
    owner_id: int

    class Config:
        orm_mode = True


class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    password: str
    tfa: bool


class User(_UserBase):
    id: int
    passwords: List[Password] = []

    class Config:
        orm_mode = True
