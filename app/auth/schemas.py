from pydantic import BaseModel


class Token(BaseModel):
    """
    Token Schema
    """

    access_token: str
    token_type: str = "bearer"
