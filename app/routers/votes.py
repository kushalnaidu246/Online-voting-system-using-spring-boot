from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Candidate, User, Vote
from ..schemas import CandidateOut, ResultOut, VoteOut
from ..security import current_user

router = APIRouter(prefix="/api/votes", tags=["votes"])


@router.get("/candidates", response_model=list[CandidateOut])
def candidates_for_voting(db: Session = Depends(get_db)):
    return db.scalars(select(Candidate).order_by(Candidate.id)).all()


@router.post("", response_model=VoteOut, status_code=status.HTTP_201_CREATED)
def cast_vote(
    candidate_id: int = Query(alias="candidateId"),
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    if db.get(Candidate, candidate_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Candidate not found")
    if db.scalar(select(Vote).where(Vote.user_id == user.id)):
        raise HTTPException(status.HTTP_409_CONFLICT, "You have already voted")
    vote = Vote(user_id=user.id, candidate_id=candidate_id)
    db.add(vote)
    try:
        db.commit()
    except IntegrityError:  # double-click / parallel requests
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "You have already voted")
    return vote


@router.get("/results", response_model=list[ResultOut])
def results(db: Session = Depends(get_db)):
    """Votes per candidate (candidates with no votes show 0), highest first."""
    count = func.count(Vote.id)
    rows = db.execute(
        select(Candidate.id, Candidate.name, count)
        .outerjoin(Vote, Vote.candidate_id == Candidate.id)
        .group_by(Candidate.id, Candidate.name)
        .order_by(count.desc(), Candidate.id)
    ).all()
    return [ResultOut(candidate_id=i, name=n, votes=c) for i, n, c in rows]
