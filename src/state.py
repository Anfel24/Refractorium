from typing import TypedDict ,List, Dict


class AgentState(TypedDict):
    files_content: Dict[str, str]  # Clé: chemin du fichier, Valeur: contenu du fichier
    target_dir: str
    iteration: int# nombre d'itérations 
    max_iterations: int # ex: 10
    analysis_report: str         # Le résultat brut de Pylint ou l'analyse de l'Auditeur
    refactoring_plan: List[str]  # La liste des étapes à suivre (JSON généré par l'IA)

    test_result:bool  # Indique si les tests unitaires ont réussi ou échoué
    test_errors:str  # Erreurs rencontrées lors de l'exécution des tests unitaires
    history: List[str]           # Un résumé des actions passées