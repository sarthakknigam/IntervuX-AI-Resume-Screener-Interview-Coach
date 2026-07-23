from agents.llm import llm
from schemas.interview_score_schema import InterviewScoreResult
from langchain_core.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=InterviewScoreResult)


def generate_interview_score(interview_answers: list, job_description: str):
    qa_block = ""

    for i, item in enumerate(interview_answers, start=1):
        if item["skipped"]:
            qa_block += f"\nQ{i}. {item['question']}\nAnswer: [SKIPPED]\n"
        else:
            qa_block += f"\nQ{i}. {item['question']}\nAnswer: {item['answer']}\n"

    prompt = f"""
You are a Senior Software Engineer and Technical Interviewer at a top product-based company (Google, Microsoft, Amazon, Atlassian, Adobe).

Your task is to evaluate a candidate's mock interview performance based ONLY on:
1. The questions asked.
2. The candidate's spoken answers (transcribed from audio, so minor grammar/transcription issues should not be penalized).
3. The job description, to judge relevance and depth.

Scoring Rules:
- Score each answer from 0 to 10 based on correctness, clarity, depth, and relevance to the job description.
- If a question was skipped, its score MUST be 0, and feedback should briefly note it was skipped without harsh judgment.
- Give short, specific, constructive feedback per answer (1-2 sentences).
- The overall_score (0-100) should reflect the candidate's aggregate performance across all questions, weighted fairly, accounting for skipped questions as 0.
- overall_feedback should be a concise, honest, constructive summary (2-4 sentences) covering strengths and areas to improve.
- Do not be needlessly harsh, but be honest and realistic like a real interviewer giving feedback.
- Return exactly one entry in question_scores per question provided, in the same order.

Job Description:
{job_description}

Interview Questions and Answers:
{qa_block}

{parser.get_format_instructions()}
"""

    try:
        response = llm.invoke(prompt)

        score = parser.parse(response.content)

        return score

    except Exception as e:
        print("Interview Scoring Error:", e)
        raise