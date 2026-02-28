
import os
import time
from pydantic import BaseModel, Field
from src.state import AgentState
from src.llm_config import get_model
from src.tools.filetools import write_file # Utilisation de tes outils
from src.tools.pylinttools import runpylint
from src.tools.pytesttools import runpytest
from src.utils.logger import log_experiment, ActionType 

llm = get_model()

class JudgeDecision(BaseModel):
    test_result: bool = Field(description="True si le code respecte tous les critères (tests + pylint)")
    test_errors: str = Field(description="Détails des échecs pour le Fixer, vide si succès")

def load_judge_prompt():
    path = os.path.join("src", "prompts", "judge_prompt.txt")
    if not os.path.exists(path):
        return "Tu es un juge QA. Valide si les tests passent et si le score pylint est bon."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def judge_node(state: AgentState):
    #time.sleep(5)
    # 1. Sauvegarde physique du code sur le disque pour que les outils puissent scanner
    print("💾 [Judge] Sauvegarde des fichiers dans la sandbox...")
    # Correction dans judge_node
    for filename, content in state["files_content"].items():
    # On reconstruit le chemin complet : sandbox/nom_du_fichier.py
     full_path = os.path.join(state["target_dir"], os.path.basename(filename))
     with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

    # 2. Exécution technique des outils
    # 2. Exécution technique des outils
    print("🔍 [Judge] Exécution de Pytest et Pylint...")
    pytest_success, pytest_logs = runpytest(state["target_dir"])
    pylint_res = runpylint(state["target_dir"])

    # FIX : Vérification si pylint_res est un dict ou un str
    if isinstance(pylint_res, dict):
        pylint_report = pylint_res.get("stdout", "")
    else:
        pylint_report = str(pylint_res)

    # 3. Appel au LLM pour le verdict final (Brain of the Judge)
    judge_prompt = load_judge_prompt()
    judge_llm = llm.with_structured_output(JudgeDecision)
    
    user_content = f"""
    RAPPORTS TECHNIQUES :
    --- PYTEST ---
    Succès: {pytest_success}
    Logs: {pytest_logs}
    
    --- PYLINT ---
    Rapport: {pylint_report}
    """

    try:
        result = judge_llm.invoke([
            {"role": "system", "content": judge_prompt},
            {"role": "user", "content": user_content}
        ])

        # --- LOGGING OBLIGATOIRE ---
        log_experiment(
            agent_name="JudgeAgent",
            model_used="gemini-1.5-flash",
            action=ActionType.GENERATION,
            details={
                "input_prompt": user_content,  
                "output_response": result.model_dump_json(),  
                "pytest_status": "PASS" if pytest_success else "FAIL",
                "pylint_report": pylint_report,
                "verdict": result.test_result
            },
            status="SUCCESS"
        )
        
        return {
            "test_result": result.test_result,
            "test_errors": result.test_errors,
            "history": state["history"] + [f"Verdict Judge: {'✅ PASS' if result.test_result else '❌ FAIL'}"]
        }

    except Exception as e:  
        error_msg = f"Erreur lors du jugement : {str(e)}"
        print(f"❌ {error_msg}")
        
        # LOGGING EN CAS D'ERREUR
        log_experiment(
            agent_name="JudgeAgent",
            model_used="gemini-1.5-flash",
            action=ActionType.GENERATION,
            details={
                "input_prompt": user_content,
                "output_response": f"ERROR: {str(e)}",
                "pytest_status": "ERROR",
                "error_details": error_msg
            },
            status="FAILURE"
        )
        
        return {
            "test_result": False,
            "test_errors": error_msg,
            "history": state["history"] + [error_msg]
        }
