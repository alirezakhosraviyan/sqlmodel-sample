from enum import Enum

from sqlmodel import Field, SQLModel


class Severity(str, Enum):
    CRITICAL = "critical"
    MEDIUM = "medium"
    LOW = "low"


class Status(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"


class Issue(SQLModel, table=True):
    """
    Issue Model representing issue table
    """

    id: int | None = Field(primary_key=True)
    description: str = Field(max_length=1000, nullable=True)
    severity: Severity
    status: Status | None = Field(default=Status.NEW)
    product_id: int | None = Field(nullable=False, foreign_key="product.id")
    assignee: str | None = Field(default=None, nullable=True, foreign_key="user.username")
    reporter: str = Field(nullable=False, foreign_key="user.username")
