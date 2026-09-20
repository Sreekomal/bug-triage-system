from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.prediction import PredictionCreate, PredictionResponse
from app.services.prediction_service import (
    create_prediction,
    get_prediction,
    get_predictions_for_bug,
)

router = APIRouter(
    prefix="/predictions",
    tags=["AI Predictions"],
)


@router.post(
    "/",
    response_model=PredictionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_prediction_endpoint(
    prediction_data: PredictionCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_prediction(db, prediction_data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while creating prediction",
        )


@router.get(
    "/{prediction_id}",
    response_model=PredictionResponse,
)
def get_prediction_by_id(
    prediction_id: int,
    db: Session = Depends(get_db),
):
    prediction = get_prediction(db, prediction_id)

    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found",
        )

    return prediction


@router.get(
    "/bug/{bug_id}",
    response_model=list[PredictionResponse],
)
def get_predictions_by_bug(
    bug_id: int,
    db: Session = Depends(get_db),
):
    return get_predictions_for_bug(db, bug_id)