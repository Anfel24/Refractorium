from src.state import AgentState
# from src.utils.tools import run_pytest (Plus tard)

def judge_node(state: AgentState):
    print(" [Judge] Vérification du code...")
    
    # Simulation : Appel à pytest via l'Ingénieur Outils
    success = False # On simule un échec pour tester la boucle
    errors = "IndentationError at line 10" if not success else ""
    
    return {
        "test_result": success,
        "test_errors": errors,
        "history": state["history"] + [f"Résultat test: {success}"]
    }