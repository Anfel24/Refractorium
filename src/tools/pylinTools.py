
    import subprocess

def runpylint(target_dir: str) -> str:
    result = subprocess.run(
        ["pylint", target_dir],
        capture_output=True,
        text=True
    )
<<<<<<< HEAD
    
 return {
         "stdout": result.stdout,
         "stderr": result.stderr,
         "returncode": result.returncode #code indique est ce que le code  la gravite de code 
    }




#Problème 2 : L'Auditeur attend probablement un texte (string) pour l'envoyer au LLM, mais ta fonction renvoie un dictionnaire {"stdout": ..., "stderr": ...}.
=======

    output = []

    if result.stdout:
        output.append("=== pylint output ===")
        output.append(result.stdout)

    if result.stderr:
        output.append("=== pylint errors ===")
        output.append(result.stderr)

    output.append(f" return code: {result.returncode} ===") #code indique est ce que le code  la gravite de code 

    return "\n".join(output)
>>>>>>> aee91c7c47513d2de751a7b7b511963a96e1803d

