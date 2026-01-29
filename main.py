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
   
   #  LOG DU DÉMARRAGE
    log_experiment(
        agent_name="SystemOrchestrator",
        model_used="N/A",
        action=ActionType.ANALYSIS,
        details={
            "input_prompt": f"Initialisation du système sur le dossier : {args.target_dir}",
            "output_response": f"Fichiers détectés : {list(files.keys())}. Prêt à démarrer.",
            "max_iterations": args.max_iterations,
            "files_count": len(files)
        },
        status="SUCCESS"
    )
    try:
     
     workflow = create_graph()
     final_state = workflow.invoke(initial_state)
     print("✅ MISSION_COMPLETE")
     print(f"Statut final : {' Corrigé' if final_state['test_result'] else 'Non corrigé'}")
     print(f"Itérations utilisées : {final_state['iteration']}/{args.max_iterations}")

      #  LOG DE FIN RÉUSSIE
     log_experiment(
            agent_name="SystemOrchestrator",
            model_used="N/A",
            action=ActionType.GENERATION,
            details={
                "input_prompt": f"Exécution complète du workflow sur {args.target_dir}",
                "output_response": f"Mission terminée. Test result: {final_state['test_result']}. Iterations: {final_state['iteration']}",
                "final_test_result": final_state['test_result'],
                "total_iterations": final_state['iteration'],
                "history": final_state.get('history', [])
            },
            status="SUCCESS"
    )
  

   

     
    except Exception as e:
    
     print(f"💥 ERREUR CRITIQUE du Graphe : {e}")
    


    #  LOG DE L'ERREUR
    log_experiment(
            agent_name="SystemOrchestrator",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": f"Tentative d'exécution du workflow sur {args.target_dir}",
                "output_response": f"ERREUR CRITIQUE: {str(e)}",
                "error_type": type(e).__name__,
                "target_dir": args.target_dir
            },
            status="FAILURE"
        )
        
sys.exit(1)

if __name__ == "__main__":
    main()