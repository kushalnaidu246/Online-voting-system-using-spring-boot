from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Candidate
from ..schemas import CandidateCreate, CandidateOut

router = APIRouter(prefix="/api/candidates", tags=["candidates"])


@router.get("", response_model=list[CandidateOut])
def list_candidates(db: Session = Depends(get_db)):
    return db.scalars(select(Candidate).order_by(Candidate.id)).all()


@router.post("", response_model=CandidateOut, status_code=status.HTTP_201_CREATED)
def add_candidate(body: CandidateCreate, db: Session = Depends(get_db)):
    candidate = Candidate(name=body.name)
    db.add(candidate)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Candidate already exists")
    return candidate
