from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.routing import APIRouter
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt.token import authorize_user
from app.auth.models import User
from app.db import session_injector
from app.issues import services
from app.issues.models import Issue
from app.issues.schemas import IssueCreate, IssueRead, IssueUpdate

router = APIRouter(prefix="/issues", tags=["issues"])


@router.post("/")
async def create_issues(
    new_issue: IssueCreate,
    authenticated_user: Annotated[User, Security(authorize_user, scopes=["issues"])],
    async_session: Annotated[AsyncSession, Depends(session_injector)],
) -> Issue:
    """
    Create a new issue.
    """
    try:
        return await services.create_issue(new_issue, async_session)
    except (NoResultFound, IntegrityError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="couldn't add issue with given data (product or reporter user doesn't exist)",
        ) from None


@router.get("/")
async def list_issues(
    authenticated_user: Annotated[User, Security(authorize_user, scopes=["issues"])],
    async_session: Annotated[AsyncSession, Depends(session_injector)],
) -> list[IssueRead]:
    """
    List all issues.
    """
    return await services.get_issues(async_session)


@router.get("/:issue_id")
async def retrieve_issue(
    issue_id: int,
    authenticated_user: Annotated[User, Security(authorize_user, scopes=["issues"])],
    async_session: Annotated[AsyncSession, Depends(session_injector)],
) -> IssueRead:
    """
    Retrieve an issue.
    """
    try:
        return await services.get_issue_by_id(issue_id, async_session)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="couldn't find issue with given id or access denied",
        ) from None


@router.patch("/{issue_id}")
async def patch_issue(
    issue_id: int,
    updated_issue: IssueUpdate,
    authenticated_user: Annotated[User, Security(authorize_user, scopes=["issues"])],
    async_session: Annotated[AsyncSession, Depends(session_injector)],
) -> Issue:
    """
    Partially update an issue.
    """
    try:
        return await services.patch_issue(issue_id, updated_issue, async_session)
    except (NoResultFound, IntegrityError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="can't update the the issue with given id and given reporter",
        ) from None
