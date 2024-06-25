import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import text

from app.auth.models import User
from app.db import get_session
from app.issues.models import Issue, Severity, Status
from app.products.models import Product


@pytest.mark.asyncio
async def test_create_issue(authenticated_test_client: TestClient, test_product: Product, test_user: User) -> None:
    session: AsyncSession
    async with get_session() as session:
        assert (await session.execute(text("select count(1) from issue"))).scalar() == 0

        res = authenticated_test_client.post(
            "api/v1/issues",
            json={
                "description": "this is a test description",
                "severity": "critical",
                "product": test_product.name,
                "reporter": test_user.username,
            },
        )

        created_issues = (await session.execute(text("select * from issue"))).all()
        # checking the response
        assert res.status_code == 200
        assert res.json() == {
            "id": 1,
            "severity": "critical",
            "status": "new",
            "description": "this is a test description",
            "product_id": 1,
            "assignee": None,
            "reporter": "test",
        }

        # checking if user is saved
        assert len(created_issues) == 1


@pytest.mark.asyncio
async def test_create_issue__invalid_product(authenticated_test_client: TestClient, test_user: User) -> None:
    session: AsyncSession
    async with get_session() as session:
        assert (await session.execute(text("select count(1) from issue"))).scalar() == 0

        res = authenticated_test_client.post(
            "api/v1/issues",
            json={
                "description": "this is a test description",
                "severity": "critical",
                "product": "wrong product",
                "reporter": test_user.username,
            },
        )
        # checking the response
        assert res.status_code == 422
        assert (await session.execute(text("select count(1) from issue"))).scalar() == 0


@pytest.mark.asyncio
async def test_create_issue__invalid_reporter(authenticated_test_client: TestClient, test_product: Product) -> None:
    session: AsyncSession
    async with get_session() as session:
        assert (await session.execute(text("select count(1) from issue"))).scalar() == 0

        res = authenticated_test_client.post(
            "api/v1/issues",
            json={"description": "this is a test description", "severity": "critical", "product": test_product.name},
        )
        # checking the response
        assert res.status_code == 422
        assert (await session.execute(text("select count(1) from issue"))).scalar() == 0


@pytest.mark.asyncio
async def test_update_issue(authenticated_test_client: TestClient, test_issue: Issue) -> None:
    session: AsyncSession
    async with get_session() as session:
        new_assignee = User(username="new_assignee", password="1234")
        session.add(new_assignee)
        await session.commit()
        await session.refresh(new_assignee)

        res = authenticated_test_client.patch(
            f"api/v1/issues/{test_issue.id}",
            json={"status": Status.IN_REVIEW, "severity": Severity.MEDIUM, "assignee": new_assignee.username},
        )
        # checking the response
        assert res.status_code == 200
        updated_issue = (await session.execute(text(f"select * from issue where id={test_issue.id}"))).one()
        assert updated_issue.status == Status.IN_REVIEW.name
        assert updated_issue.severity == Severity.MEDIUM.name
        assert updated_issue.assignee == new_assignee.username


@pytest.mark.asyncio
async def test_update_issue__partially(authenticated_test_client: TestClient, test_issue: Issue) -> None:
    session: AsyncSession
    async with get_session() as session:
        res = authenticated_test_client.patch(
            f"api/v1/issues/{test_issue.id}",
            json={"status": Status.IN_REVIEW},
        )
        # checking the response
        assert res.status_code == 200
        updated_issue = (await session.execute(text(f"select * from issue where id={test_issue.id}"))).one()
        assert updated_issue.status == Status.IN_REVIEW.name


@pytest.mark.asyncio
async def test_get_issues(authenticated_test_client: TestClient, test_issue: Issue) -> None:
    issues = [Issue(**test_issue.model_dump(exclude={"id"})) for _ in range(0, 3)]
    session: AsyncSession
    async with get_session() as session:
        session.add_all(issues)
        await session.commit()

    res = authenticated_test_client.get("api/v1/issues")

    assert len(res.json()) == 4  # 3 + 1 --> new + old(from fixture)
