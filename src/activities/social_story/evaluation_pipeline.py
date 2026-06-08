import re
from pydantic import BaseModel

class DeterministicAnalysisReport(BaseModel):
    second_person_pronouns: bool
    absolute_constraints: bool

def deterministic_analysis(story_text: str) -> DeterministicAnalysisReport:
    # 1. Define clean regex target groups
    pronoun_patterns = [r"\byou\b", r"\byour\b", r"\byours\b"]
    constraint_patterns = [r"\bmust\b", r"\bshould\b", r"\balways\b", r"\bnever\b"]
    
    # 2. Evaluate both conditions completely across the text
    has_pronouns = any(
        bool(re.search(pattern, story_text, re.IGNORECASE)) 
        for pattern in pronoun_patterns
    )
    
    has_constraints = any(
        bool(re.search(pattern, story_text, re.IGNORECASE)) 
        for pattern in constraint_patterns
    )
    
    # 3. Instantiate and return your actual Pydantic class
    return DeterministicAnalysisReport(
        second_person_pronouns=has_pronouns,
        absolute_constraints=has_constraints
    )
