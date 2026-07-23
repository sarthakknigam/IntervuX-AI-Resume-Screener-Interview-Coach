from typing import List, Optional
from pydantic import BaseModel

class ATSResult(BaseModel):
    ats_score: int

    hiring_decision: str

    matching_skills: List[str] = []

    missing_skills: List[str] = []

    strengths: List[str] = []

    weaknesses: List[str] = []

    suggestions: List[str] = []

    summary: Optional[str] = None