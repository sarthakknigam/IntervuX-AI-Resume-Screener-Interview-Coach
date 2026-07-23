from agents.llm import llm
from schemas.resume_schema import Resume

structured_llm = llm.with_structured_output(Resume)

def parse_resume(resume_text: str):
    prompt = f"""
Extract the following information from this resume.

Resume:
{resume_text}
"""

    return structured_llm.invoke(prompt)