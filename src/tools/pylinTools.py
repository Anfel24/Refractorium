
import subprocess

def runpylint(target_dir: str) -> str:
    result = subprocess.run(
        ["pylint", target_dir],
        capture_output=True,
        text=True
    )

    
    return {
         "stdout": result.stdout,
         "stderr": result.stderr,
         "returncode": result.returncode #code indique est ce que le code  la gravite de code 
    }




#Problème 2 : L'Auditeur attend probablement un texte (string) pour l'envoyer au LLM, mais ta fonction renvoie un dictionnaire {"stdout": ..., "stderr": ...}.

