import argparse
import sys
import os

from dotenv import load_dotenv
from graph import create_graph
from src.utils.logger import log_experiment
from state import AgentState
import src.tools.fileTools as tools

load_dotenv()



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True)
    parser.add_argument("--max_iterations", type=int, default=10) #  10 par défaut
    args = parser.parse_args()

    if not os.path.exists(args.target_dir):
        print(f"❌ Dossier {args.target_dir} introuvable.")
        sys.exit(1)
    
    # INITIALISATION 
    
    initial_state: AgentState = {
        "target_dir": args.target_dir,
        "max_iterations": args.max_iterations,
        "iteration": 0,                # On commence à zéro
        "files_content": tools.read_file(args.target_dir),          
        "analysis_report": "",
        "refactoring_plan": [],
        "test_result": False,
        "test_errors": "",
        "history": ["Démarrage du système"]
    }


    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")
    log_experiment("System", "STARTUP", f"Target: {args.target_dir}", "INFO")
 

    workflow = create_graph()
    final_state = workflow.invoke(initial_state)
    print("✅ MISSION_COMPLETE")

if __name__ == "__main__":
    main()