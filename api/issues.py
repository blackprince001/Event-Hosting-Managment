import datetime

from sqlalchemy import update
from sqlalchemy.orm import Session

from schemas.issues import IssueCreate
from database.models import Issues as IssuesModel


def create_issues(db: Session, new_issue: IssueCreate) -> IssuesModel:
    db_issue = IssuesModel(**new_issue.dict())

    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)

    return db_issue


def get_issue(db: Session, issues_id: int) -> IssuesModel | None:
    return db.get(IssuesModel, issues_id)


def set_issue_resolved(db: Session, issue_id: int, date: datetime, state: bool):
    if state:
        return db.execute(
            update(IssuesModel)
            .where(IssuesModel.id == issue_id)
            .values(is_resolved=True, dt_resolved=date)
        )

    return get_issue(db=db, issues_id=issue_id)


def update_issues_statement(db: Session, issue_id: int, new_statement: str):
    return db.execute(
        update(IssuesModel)
        .where(IssuesModel.id == issue_id)
        .values(statement=new_statement)
    )
