from sqlalchemy.orm import Session

from app.models.bug import Bug
from app.models.prediction import AIPrediction
from app.schemas.prediction import PredictionCreate


def create_prediction(
    db: Session,
    prediction_data: PredictionCreate
) -> AIPrediction:

    # Make sure the bug exists
    bug = (
        db.query(Bug)
        .filter(Bug.id == prediction_data.bug_id)
        .first()
    )

    if not bug:
        raise ValueError("Bug not found")

    prediction = AIPrediction(
        bug_id=prediction_data.bug_id,
        predicted_category=prediction_data.predicted_category,
        predicted_severity=prediction_data.predicted_severity,
        duplicate_bug=prediction_data.duplicate_bug,
        confidence_score=prediction_data.confidence_score,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction


def get_prediction(
    db: Session,
    prediction_id: int
) -> AIPrediction | None:

    return (
        db.query(AIPrediction)
        .filter(AIPrediction.id == prediction_id)
        .first()
    )


def get_predictions_for_bug(
    db: Session,
    bug_id: int
) -> list[AIPrediction]:

    return (
        db.query(AIPrediction)
        .filter(AIPrediction.bug_id == bug_id)
        .all()
    )