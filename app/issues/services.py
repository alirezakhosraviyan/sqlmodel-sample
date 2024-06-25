from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.products.models import Product
from app.products.services import get_product_by_name

from .models import Issue
from .schemas import IssueCreate, IssueRead, IssueUpdate


async def create_issue(new_issue: IssueCreate, async_session: AsyncSession) -> Issue:
    product = await get_product_by_name(new_issue.product, async_session)
    issue = Issue(**new_issue.model_dump(exclude={"product"}), product_id=product.id)
    async_session.add(issue)
    await async_session.commit()
    await async_session.refresh(issue)
    return issue


async def patch_issue(issue_id: int, updated_issue: IssueUpdate, async_session: AsyncSession) -> Issue:
    # based on the standard docs from sqlmodel, updating data can be done with a read and save
    stmt = select(Issue).where(Issue.id == issue_id)
    issue: Issue = (await async_session.execute(stmt)).one()[0]

    # making abstraction for updating data
    # any field coming from IssueUpdate which has a value can amend issue table's data if row exists
    for k, v in updated_issue.model_dump(exclude_unset=True, exclude_none=True).items():
        issue.__setattr__(k, v)

    await async_session.commit()
    await async_session.refresh(issue)
    return issue


async def get_issue_by_id(issue_id: int, async_session: AsyncSession) -> IssueRead:
    """
    fetch issue by id
    """
    stmt = select(Issue, Product).where(Issue.id == issue_id).join(Product)
    retrieved_data = (await async_session.execute(stmt)).one()
    return IssueRead(
        product=retrieved_data[1].name,
        id=retrieved_data[0].id,
        reporter=retrieved_data[0].reporter,
        status=retrieved_data[0].status,
        severity=retrieved_data[0].severity,
        assignee=retrieved_data[0].assignee,
        description=retrieved_data[0].description,
    )


async def get_issues(async_session: AsyncSession) -> list[IssueRead]:
    """
    fetch all issues
    TODO(alireza): pagination must be added here (cursor method instead of offset)
    """
    stmt = select(Issue, Product).join(Product)
    return [
        IssueRead(
            product=retrieved_data[1].name,
            id=retrieved_data[0].id,
            reporter=retrieved_data[0].reporter,
            status=retrieved_data[0].status,
            severity=retrieved_data[0].severity,
            assignee=retrieved_data[0].assignee,
            description=retrieved_data[0].description,
        )
        for retrieved_data in (await async_session.execute(stmt)).all()
    ]
