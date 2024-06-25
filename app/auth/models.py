from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """
    Schema of User Model (equivalent to pydantic model)
    """

    username: str | None = Field(max_length=255, nullable=False, primary_key=True)
    fullname: str = Field(default="", max_length=255)
    password: str

    class Config:
        json_schema_extra = {"example": {"username": "alireza", "fullname": "Alireza Khosravian", "password": "1234"}}


class User(UserBase, table=True):
    """
    User Table Model
    """

    active: bool = True
