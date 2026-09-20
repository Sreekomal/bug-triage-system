from sqlalchemy.orm import Session

from app.models.bug import Bug
from app.schemas.bug import BugCreate, BugUpdate


def create_bug(db: Session, bug_data: BugCreate) -> Bug:
    new_bug = Bug(
        title=bug_data.title,
        description=bug_data.description,
        steps_to_reproduce=bug_data.steps_to_reproduce,
        environment=bug_data.environment,
        status=bug_data.status,
        created_by=bug_data.created_by,
        assigned_to=bug_data.assigned_to,
    )

    db.add(new_bug)
    db.commit()
    db.refresh(new_bug)

    return new_bug


def get_bug(db: Session, bug_id: int) -> Bug | None:
    return (
        db.query(Bug)
        .filter(Bug.id == bug_id)
        .first()
    )


def get_bugs(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> list[Bug]:
    return (
        db.query(Bug)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_bug(
    db: Session,
    bug_id: int,
    bug_data: BugUpdate
) -> Bug | None:

    bug = get_bug(db, bug_id)

    if not bug:
        return None

    update_data = bug_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(bug, field, value)

    db.commit()
    db.refresh(bug)

    return bug


def delete_bug(db: Session, bug_id: int) -> bool:
    bug = get_bug(db, bug_id)

    if not bug:
        return False

    db.delete(bug)
    db.commit()

    return True