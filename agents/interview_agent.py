from agents.llm import llm
from schemas.interview_schema import InterviewQuestion
from langchain_core.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=InterviewQuestion)


def generate_interview_questions(resume_text: str, job_description: str):
    prompt = f"""
You are a Senior Software Engineer and Technical Interviewer at a top product-based company (Google, Microsoft, Amazon, Atlassian, Adobe).

Your task is to create interview questions for this candidate based ONLY on:
1. The candidate's resume.
2. The provided job description.

Generate the following:

1. Technical Questions
- Generate exactly 5 technical interview questions.
- Base them on the candidate's skills and the technologies required in the job description.
- Questions should start from intermediate level and gradually become difficult.
- Ask conceptual and practical questions.
- Avoid generic questions.

2. Project Questions
- Generate exactly 5 questions ONLY from the projects mentioned in the candidate's resume.
- Mention the project name in every question whenever possible.
- Ask about:
  - Architecture
  - Design decisions
  - Algorithms used
  - Tech stack
  - Database design
  - APIs
  - AI/ML models (if applicable)
  - Challenges faced
  - Performance optimization
  - Deployment
  - Scalability
  - Future improvements
- If multiple projects exist, generate questions from different projects.
- NEVER generate generic project questions.
- If only one project exists, ask increasingly deeper questions about that project.

3. HR Questions
- Generate exactly 5 HR questions.
- Questions should evaluate communication, teamwork, leadership, conflict resolution, adaptability, learning ability, and career goals.
- Avoid cliché questions unless necessary.

Rules:
- Generate exactly 5 questions in each category.
- Do not repeat any question.
- Questions should sound like they are asked in a real technical interview.
- Keep each question concise (one or two sentences).
- Return the output in the required structured format only.

Candidate Resume:
{resume_text}

Job Description:
{job_description}

{parser.get_format_instructions()}
"""

    try:
        response = llm.invoke(prompt)

        questions = parser.parse(response.content)

        return questions

    except Exception as e:
        print("Interview Generation Error:", e)
        raise