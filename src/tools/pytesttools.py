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

