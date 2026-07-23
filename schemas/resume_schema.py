from typing import List, Optional
from pydantic import BaseModel

class Resume(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    skills: List[str] = []
    education: List[str] = []
    projects: List[str] = []
    experience: List[str] = []