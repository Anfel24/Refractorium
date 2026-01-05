from src.state import AgentState
# from src.prompts.auditor import AUDITOR_PROMPT (Plus tard)

def auditor_node(state: AgentState):
    print(" [Auditeur] Analyse du code en cours...")
    # Simulation de l'appel LLM
    report = "Diagnostic : Manque de docstrings et complexité élevée."
    plan = ["Ajouter des docstrings", "Refactoriser les fonctions longues"]
    
    return {
        "analysis_report": report,
        "refactoring_plan": plan,
        "history": state["history"] + ["Audit terminé"]
    }