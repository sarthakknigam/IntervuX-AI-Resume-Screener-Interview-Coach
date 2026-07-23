from agents.llm import llm
from schemas.ats_schema import ATSResult

structured_llm = llm.with_structured_output(ATSResult)

def ats_match(resume_text: str, job_description: str):

    prompt = f"""
You are an expert ATS Resume Screening System.

Compare the resume with the job description.

Return:

1. ATS Score (0-100)

2. Matching Skills

3. Missing Skills

4. Candidate Strengths

5. Candidate Weaknesses

Return at least 3 concise weaknesses based only on the resume and job description.

Examples:
- No internship experience
- Missing Docker experience
- No cloud deployment experience
- Limited backend development experience
- No Spring Boot projects
- No professional work experience

Always return at least three weaknesses

6. Suggestions to improve resume

7. One paragraph summary.

Resume

{resume_text}


Job Description

{job_description}

"""

    return structured_llm.invoke(prompt)