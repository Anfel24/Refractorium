from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.nodes.auditor import auditor_node
from src.nodes.fixer import fixer_node
from src.nodes.judge import judge_node

def should_continue(state: AgentState):
    # La logique de routage de l'Orchestrateur
    if state["test_result"] == True:
        print(" Code validé !")
        return END
    
    if state["iteration"] >= state["max_iterations"]:
        print(" Échec : Nombre maximum d'itérations atteint.")
        return END
    
    print(" Retour au Correcteur pour une nouvelle tentative.")
    return "fixer"

def create_graph():
    workflow = StateGraph(AgentState)

    # Ajout des nœuds
    workflow.add_node("auditor", auditor_node)
    workflow.add_node("fixer", fixer_node)
    workflow.add_node("judge", judge_node)

    # Définition des liens
    workflow.add_edge(START, "auditor")
    workflow.add_edge("auditor", "fixer")
    workflow.add_edge("fixer", "judge")

    # La boucle conditionnelle
    workflow.add_conditional_edges(
        "judge",
        should_continue,
        {END: END, "fixer": "fixer"} # Mappage des sorties
    )

    return workflow.compile()