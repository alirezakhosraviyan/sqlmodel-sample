from pydantic import BaseModel

from app.issues.models import Severity, Status


class IssueCreate(BaseModel):
    """
    Schema for issue creation
    """

    description: str
    severity: Severity
    product: str
    reporter: str


class IssueUpdate(BaseModel):
    """
    Schema for issue update
    """

    severity: Severity | None = None
    status: Status | None = None
    assignee: str | None = None


class IssueRead(BaseModel):
    """
    Schema for issue read
    """

    id: int
    product: str
    severity: Severity
    status: Status
    assignee: str | None = None
    reporter: str
    description: str
