# code_to_fix.py

"""
Ce module est volontairement mal Ã©crit pour tester l'orchestrateur.
Il manque de docstrings, utilise de mauvais noms et contient un bug.
"""

def Addition(A, b):
    # Pylint va rÃ¢ler : mauvais nom (A), manque de docstring, 
    # et peut-Ãªtre des espaces manquants autour de '='.
    rÃ©sultat=A+b
    return rÃ©sultat

def test_addition():
    # Pytest va Ã©chouer ici car l'assertion est fausse.
    # Cela forcera l'agent 'Fixer' Ã  intervenir.
    assert Addition(2, 3) == 6