import os  # FIX 1: Import manquant
from src.state import AgentState
from src.tools.pylinTools import runpylint
from llm_config import get_model
from pydantic import BaseModel, Field
# FIX 3: Import du logger obligatoire
from src.utils.logger import log_experiment, ActionType 

llm = get_model()

class RefactoringPlan(BaseModel):
    priority: str = Field(description="Niveau de priorité global du refactoring (CRITICAL/HIGH/MEDIUM/LOW)")
    summary: str = Field(description="Résumé rapide de l'état du code")
    steps: list[str] = Field(description="Liste détaillée des actions")

def load_auditor_prompt():
    path = os.path.join("src", "prompts", "auditor_prompt.txt")
    if not os.path.exists(path):
        return "Tu es un expert Python. Analyse le code et propose un plan de refactoring."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Chargement initial du prompt
AUDITOR_SYSTEM_PROMPT = load_auditor_prompt()

def auditor_node(state: AgentState):
    # Récupération du dict Pylint
    pylint_res = runpylint(state["target_dir"])
    
    # FIX 2: On formate les erreurs pour le LLM
    pylint_report = pylint_res.get("stdout", "Aucune erreur détectée.")
    
    auditor_llm = llm.with_structured_output(RefactoringPlan)
    
    # Préparation du contenu utilisateur pour le log et le LLM
    user_content = f"Fichiers:\n{state['files_content']}\n\nApport Pylint:\n{pylint_report}"
    
    try:
        print("🧠 [Auditor] Génération du plan...")
        result = auditor_llm.invoke([
            {"role": "system", "content": AUDITOR_SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ])
        
        if not result:
            raise ValueError("L'IA n'a pas pu générer de plan structuré.")

        # FIX 3: LOGGING OBLIGATOIRE POUR LE TP
        log_experiment(
            agent_name="AuditorAgent",
            model_used="gemini-1.5-flash", # ou votre modèle
            action=ActionType.ANALYSIS,
            details={
                "input_prompt": user_content,
                "output_response": result.model_dump_json()
            },
            status="SUCCESS"
        )

        return {
            "analysis_report": pylint_report,
            "refactoring_plan": result.steps,
            "history": state["history"] + [f"Audit terminé (Priorité: {result.priority})"]
        }

    except Exception as e:
        error_msg = f"Audit échoué : {str(e)}"
        print(f"❌ {error_msg}")
        
        # Log de l'échec
        log_experiment(
            agent_name="AuditorAgent",
            model_used="gemini-1.5-flash",
            action=ActionType.ANALYSIS,
            details={"error": str(e)},
            status="FAILED"
        )
        
        return {
            "analysis_report": pylint_report,
            "refactoring_plan": ["Corriger les erreurs Pylint manuellement"],
            "history": state["history"] + [error_msg]
        }