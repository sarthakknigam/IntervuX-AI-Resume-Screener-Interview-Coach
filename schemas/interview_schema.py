from typing import List
from pydantic import BaseModel, Field

class InterviewQuestion(BaseModel):
    Technical_Questions: List[str] = Field(default_factory=list)
    HR_Questions: List[str] = Field(default_factory=list)
    Project_Questions: List[str] = Field(default_factory=list)