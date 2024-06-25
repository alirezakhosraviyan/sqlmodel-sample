from sqlmodel import Field, SQLModel


class ProductBase(SQLModel):
    """
    Product Schema for creating a new instance
    """

    name: str = Field(min_length=3, max_length=500, nullable=False, unique=True)


class Product(ProductBase, table=True):
    """
    Product Model representing product table
    """

    id: int | None = Field(primary_key=True)
