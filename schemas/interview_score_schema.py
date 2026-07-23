from pydantic import BaseModel, Field
from typing import List


class QuestionScore(BaseModel):
    question: str = Field(description="The interview question that was asked")
    answer: str = Field(description="The candidate's answer, or empty string if skipped")
    skipped: bool = Field(description="True if the candidate skipped this question")
    score: int = Field(description="Score out of 10 for this answer. Use 0 if skipped.")
    feedback: str = Field(description="Short, specific feedback on this answer. If skipped, say so briefly.")


class InterviewScoreResult(BaseModel):
    overall_score: int = Field(description="Overall interview score out of 100")
    overall_feedback: str = Field(description="2-4 sentence overall summary of the candidate's interview performance")
    question_scores: List[QuestionScore] = Field(description="Per-question scores and feedback, in the same order as given")