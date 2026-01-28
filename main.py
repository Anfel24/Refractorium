import argparse
import sys
import os

from dotenv import load_dotenv
from src.graph import create_graph
from src.utils.logger import log_experiment, ActionType
from src.state import AgentState
import src.tools.filetools as tools

load_dotenv()



def main():
    print(f"DEBUG: Ma clé commence par: {str(os.getenv('GOOGLE_API_KEY'))[:10]}...")
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True)
    parser.add_argument("--max_iterations", type=int, default=10) #  10 par défaut
    args = parser.parse_args()

    if not os.path.exists(args.target_dir):
        print(f"❌ Dossier {args.target_dir} introuvable.")
        sys.exit(1)
    
    # Validation du dossier
    if not os.path.isdir(args.target_dir):
        print(f" Erreur : '{args.target_dir}' n'est pas un dossier valide.")
        sys.exit(1)
    
    # Lecture initiale des fichiers 
    files = tools.read_file(args.target_dir)
    if not files:
        print(" Aucun fichier Python trouvé dans le dossier cible. Fin du programme.")
        sys.exit(0)
    # INITIALISATION 
    
    initial_state: AgentState = {
        "target_dir": args.target_dir,
        "max_iterations": args.max_iterations,
        "iteration": 0,                # On commence à zéro
        "files_content": files,          
        "analysis_report": "",
        "refactoring_plan": [],
        "test_result": False,
        "test_errors": "",
        "history": ["Démarrage du système"]
    }


    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")
    #format irronne :should be fixed 
   # log_experiment("System", "STARTUP", f"Target: {args.target_dir}", "INFO" ,"STARTING")
    details_startup = {
    "input_prompt": "Initialisation du système",
    "output_response": f"Dossier cible détecté : {args.target_dir}"
}
    log_experiment(
    agent_name="System",
    model_used="None",
    action=ActionType.ANALYSIS, # Utilise l'Enum !
    details=details_startup,    # Envoie le dictionnaire avec les clés requises !
    status="SUCCESS"
)
    try:
     workflow = create_graph()
     final_state = workflow.invoke(initial_state)
     print("✅ MISSION_COMPLETE")
     print(f"Statut final : {' Corrigé' if final_state['test_result'] else 'Non corrigé'}")
     print(f"Itérations utilisées : {final_state['iteration']}/{args.max_iterations}")
  

    except Exception as e:
     print(f"💥 ERREUR CRITIQUE du Graphe : {e}")
     """log_experiment(
        agent_name="System", 
        model_used="N/A", 
        action=ActionType.ANALYSIS, 
        details={"input_prompt": "Crash Système", "output_response": str(e)}, 
        status="FAILURE"
    )"""

   



if __name__ == "__main__":
    main()