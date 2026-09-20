from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.bug import BugCreate, BugResponse, BugUpdate
from app.services.bug_service import (
    create_bug,
    delete_bug,
    get_bug,
    get_bugs,
    update_bug,
)

router = APIRouter(
    prefix="/bugs",
    tags=["Bugs"],
)


@router.post(
    "/",
    response_model=BugResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_bug_endpoint(
    bug_data: BugCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_bug(db, bug_data)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while creating bug",
        )


@router.get(
    "/",
    response_model=list[BugResponse],
)
def get_all_bugs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_bugs(db, skip=skip, limit=limit)


@router.get(
    "/{bug_id}",
    response_model=BugResponse,
)
def get_bug_by_id(
    bug_id: int,
    db: Session = Depends(get_db),
):
    bug = get_bug(db, bug_id)

    if not bug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bug not found",
        )

    return bug


@router.put(
    "/{bug_id}",
    response_model=BugResponse,
)
def update_bug_by_id(
    bug_id: int,
    bug_data: BugUpdate,
    db: Session = Depends(get_db),
):
    try:
        bug = update_bug(db, bug_id, bug_data)

        if not bug:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bug not found",
            )

        return bug

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while updating bug",
        )


@router.delete(
    "/{bug_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_bug_by_id(
    bug_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_bug(db, bug_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bug not found",
        )

    return None