from src.state import AgentState
from src.tools import save_files_to_disk, runpytest

def judge_node(state: AgentState):
    
    # Écrire le code du State sur le disque
   
    try:
        #khouloud:i need this function to save the files to disk before running tests
        save_files_to_disk(state["target_dir"], state["files_content"])
        
        # EXÉCUTION DES TESTS
        
        test_success, logs = runpytest(state["target_dir"])
        
        if test_success:
            print("  Tous les tests passent !")
            summary = "Le code est valide et fonctionnel."
        else:
            print(f"Échec des tests : {logs[:100]}...")
            summary = f"Erreurs détectées : {logs}"

        #  MISE À JOUR DE L'ÉTAT
        return {
            "test_result": True if test_success else False,
            "test_errors": logs if not test_success else "",
            "history": state["history"] + [f"Jugement : {summary}"]
        }

    except Exception as e:
        error_msg = f"Erreur technique lors du jugement : {str(e)}"
        print(f"{error_msg}")
        return {
            "test_result": False,
            "test_errors": error_msg,
            "history": state["history"] + [error_msg]
        }