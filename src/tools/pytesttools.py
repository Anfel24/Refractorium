


import subprocess

def runpytest(target_dir: str):
    result = subprocess.run(
        ["pytest", target_dir],
        capture_output=True,
        text=True
    )

    success = (result.returncode == 0)  #si sup a 0 donc ya des test qui echoue 

    logs = []
    logs.append("===== rapport de pytest =====")

    if result.stdout.strip(): 
        logs.append("---- sortie standard ----")# imprime tout ce que ce outil donne les resultats des tests 
        logs.append(result.stdout)

    if result.stderr.strip():
        logs.append("---- erreurs ----")  #les erreurs taper par l'outil 
        logs.append(result.stderr)

    logs.append(f"---- le code: {result.returncode} ----") 

    return success, "\n".join(logs)
