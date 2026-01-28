import os
import time
from pydantic import BaseModel, Field
from src.state import AgentState
from src.llm_config import get_model
from typing import Dict
# Importation du logger obligatoire pour le TP
from src.utils.logger import log_experiment, ActionType 

llm = get_model()

class FixedCode(BaseModel):
    files_content: Dict[str, str] = Field(
        description="Dictionnaire complet des fichiers modifiés {nom_fichier: contenu_complet}"
    )
    explanation: str = Field(description="Résumé technique des corrections effectuées")

def load_fixer_prompt():
    """Charge les instructions système depuis le fichier texte externe"""
    path = os.path.join("src", "prompts", "fixer_prompt.txt")
    if not os.path.exists(path):
        return "Tu es un expert Python. Applique le plan de refactoring fourni."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def fixer_node(state: AgentState):
    #time.sleep(5)
    # Incrémentation de l'itération
    new_iteration = state.get("iteration", 0) + 1
    
    # Préparation du prompt système
    FIXER_SYSTEM_PROMPT = load_fixer_prompt()
    
    # Configuration du LLM structuré
    fixer_llm = llm.with_structured_output(FixedCode)

    # Préparation des données pour le prompt utilisateur
    plan_str = "\n".join(state.get("refactoring_plan", ["Aucun plan fourni"]))
    last_errors = state.get("test_errors", "Aucune erreur précédente.")
    current_code = str(state.get("files_content", {}))
    
    user_content = f"""
    PLAN À SUIVRE : 
    {plan_str}
    
    ERREURS DE TESTS À CORRIGER : 
    {last_errors}
    
    CODE SOURCE ACTUEL : 
    {current_code}
    """

    try:
        print(f"🛠️ [Fixer] Itération {new_iteration} : Application des corrections...")
        
        # Appel au LLM
        result = fixer_llm.invoke([
            {"role": "system", "content": FIXER_SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ])

        if not result or not result.files_content:
            raise ValueError("L'IA a renvoyé un contenu vide ou invalide.")

        # --- LOGGING OBLIGATOIRE (Critère de notation Data-Driven) ---
        log_experiment(
            agent_name="FixerAgent",
            model_used="gemini-2.0-flash", # ou votre modèle config
            action=ActionType.FIX,
            details={
                "input_prompt": user_content,
                "output_response": result.model_dump_json(),
                "iteration": new_iteration
            },
            status="SUCCESS"
        )
        # -----------------------------------------------------------

        # Mise à jour sécurisée des fichiers
        updated_files = state["files_content"].copy()
        updated_files.update(result.files_content)

        return {
            "iteration": new_iteration,
            "files_content": updated_files,
            "history": state["history"] + [f"Correction {new_iteration}: {result.explanation}"]
        }

    except Exception as e:
        error_msg = f"Échec de la correction : {str(e)}"
        print(f"❌ {error_msg}")
        
        # Log de l'échec
        log_experiment(
            agent_name="FixerAgent",
            model_used="gemini-1.5-flash",
            action=ActionType.FIX,
            details={"error": str(e), "iteration": new_iteration},
            status="FAILED"
        )
        
        return {
            "iteration": new_iteration,
            "history": state["history"] + [error_msg]
        }