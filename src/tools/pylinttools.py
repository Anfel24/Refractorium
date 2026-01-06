

import subprocess

def runpytest(target_dir: str):
    result = subprocess.run(
        ["pytest", target_dir],
        capture_output=True,
        text=True
    )

    success = (result.returncode == 0)

    logs = []
    logs.append("===== rapport de pytest =====")

    if result.stdout.strip():
        logs.append("---- sortie standard ----")
        logs.append(result.stdout)

    if result.stderr.strip():
        logs.append("---- erreurs ----")
        logs.append(result.stderr)

    logs.append(f"---- le code: {result.returncode} ----") #code indique est ce que le code  la gravite de code 

    return success, "\n".join(logs)
