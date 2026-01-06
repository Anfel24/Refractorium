from src.state import AgentState
from src.tools.pylinTools import runpylint
from llm_config import get_model
from pydantic import BaseModel, Field


llm=get_model()

#un exemple pour Sihem (ingenieure prompt) sur la definition de model de sortie structuré avec pydantic
class RefactoringPlan(BaseModel):
    priority: str = Field(description="High/Medium/Low")
    steps: list[str] = Field(description="Liste des actions à faire")

AUDITOR_SYSTEM_PROMPT = "Tu es un expert Python. Analyse ces fichiers..."



def auditor_node(state: AgentState):
    pylint_errors = runpylint(state["target_dir"])
   
    
    # Configuration de la sortie structurée pour Gemini
    auditor_llm = llm.with_structured_output(RefactoringPlan)
    
    try:
        print("🧠 [Auditor] Génération du plan de refactoring...")
        result = auditor_llm.invoke([
            {"role": "system", "content": AUDITOR_SYSTEM_PROMPT},
            {"role": "user", "content": f"Fichiers: {state['files_content']}\n\nErreurs Pylint: {pylint_errors}"}
        ])
        
        # Sécurité : On vérifie que l'IA a bien répondu
        if not result:
            raise ValueError("L'IA n'a pas pu générer de plan structuré.")

        return {
            "analysis_report": pylint_errors,
            "refactoring_plan": result.steps,
            "history": state["history"] + [f"Audit terminé (Priorité: {result.priority})"]
        }

    except Exception as e:
        error_msg = f"Audit échoué : {str(e)}"
        print(f"❌ {error_msg}")
        return {
            "analysis_report": pylint_errors,
            "refactoring_plan": ["Corriger les erreurs Pylint manuellement"], # Fallback
            "history": state["history"] + [error_msg]
        }