import subprocess

def runpytest(target_dir):
  result = subprocess.run(
         ["pytest", target_dir],
         capture_output=True,
         text=True
    )
  return {
     "success": result.returncode == 0, #si sup a 0 donc ya des test qui echoue 
         "stdout": result.stdout,# imprime tout ce que ce outil donne les resultats des tests 
        "stderr": result.stderr #les erreurs taper par l'outil 
    }


#Pytest peut être très bavard. Pour le Judge (et surtout pour le Fixer qui lira ces erreurs ensuite), nous avons besoin de voir quels tests ont échoué et pourquoi.
#attend probablement un texte (string) pour l'envoyer au LLM, mais ta fonction renvoie un dictionnaire {"stdout": ..., "stderr": ...}.