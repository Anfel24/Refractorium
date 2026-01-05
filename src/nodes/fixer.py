from pydantic import BaseModel, Field
from src.state import AgentState
from src.llm_config import get_model
from typing import Dict


llm = get_model()
#un exemple pour Sihem (ingenieure prompt) sur la definition de model de sortie structuré avec pydantic
class FixedCode(BaseModel):
    files_content: Dict[str, str] = Field(
        description="Le dictionnaire complet des fichiers modifiés {nom_fichier: contenu}"
    )
    explanation: str = Field(description="Résumé des corrections effectuées")

FIXER_SYSTEM_PROMPT = """Tu es un développeur Python expert en refactoring.
Ta mission est d'appliquer STRICTEMENT le plan de refactoring fourni.
Tu dois renvoyer le contenu COMPLET de chaque fichier modifié. 
Ne change pas la logique métier, améliore uniquement la structure et la qualité selon le plan."""



def fixer_node(state: AgentState):
    # Incrémentation de l'itération 
    new_iteration = state["iteration"] + 1
    
    # On prépare le LLM structuré
    fixer_llm = llm.with_structured_output(FixedCode)

    # Construction de la requête
    # Note comment on injecte le plan de l'auditeur ici !
    plan_str = "\n".join(state["refactoring_plan"])
    
    try:
        result = fixer_llm.invoke([
            {"role": "system", "content": FIXER_SYSTEM_PROMPT},
            {"role": "user", "content": f"""
                PLAN À SUIVRE : 
                {plan_str}
                
                CODE ACTUEL : 
                {state['files_content']}
            """}
        ])

       # On vérifie si result est None ou si files_content est vide
        if not result or not result.files_content:
            raise ValueError("L'IA a renvoyé un contenu vide ou invalide.")

        # Mise à jour de l'état
        return {
            "iteration": new_iteration,
            "files_content": result.files_content, # Le code est maintenant mis à jour !
            "history": state["history"] + [f"Correction {new_iteration}: {result.explanation}"]
        }

    except Exception as e:
        print(f" Erreur lors de la correction : {e}")
        return {
            "iteration": new_iteration,
            "history": state["history"] + [f"Échec de la correction n°{new_iteration}"]
        }