from src.state import AgentState
from tools.pylinTools import runpylint
from llm_config import get_model
from pydantic import BaseModel, Field


llm=get_model()

#un exemple pour Sihem (ingenieure prompt) sur la definition de model de sortie structuré avec pydantic
class RefactoringPlan(BaseModel):
    priority: str = Field(description="High/Medium/Low")
    steps: list[str] = Field(description="Liste des actions à faire")

AUDITOR_SYSTEM_PROMPT = "Tu es un expert Python. Analyse ces fichiers..."



def auditor_node(state: AgentState):
    pylint_errors = runpylint(state["files_content"])
    auditor_llm = llm.with_structured_output(RefactoringPlan)
    result = auditor_llm.invoke([
        {"role": "system", "content": AUDITOR_SYSTEM_PROMPT},
        {"role": "user", "content": f"Voici les fichiers: {state['files_content']} et les erreurs: {pylint_errors}"}
    ])
    
    return {
        "analysis_report": pylint_errors,
         "refactoring_plan": result.steps,
        "history": state["history"] + ["Audit terminé"]
    }