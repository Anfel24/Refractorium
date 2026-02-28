<<<<<<< HEAD
import subprocess

def runpylint(target_dir: str) -> str:
    result = subprocess.run(
        ["pylint", target_dir],
        capture_output=True,
        text=True
    )

    output = []

    if result.stdout:
        output.append("=== dortie de pylint ===")
        output.append(result.stdout)

    if result.stderr:
        output.append("=== pylint erreurs ===")
        output.append(result.stderr)

    output.append(f"=== le code: {result.returncode} ===") #code indique est ce que le code  la gravite de code 

    return "\n".join(output)
=======
import subprocess

def runpylint(target_dir: str) -> str:
    result = subprocess.run(
        ["pylint", target_dir],
        capture_output=True,
        text=True
    )

    output = []

    if result.stdout:
        output.append("=== dortie de pylint ===")
        output.append(result.stdout)

    if result.stderr:
        output.append("=== pylint erreurs ===")
        output.append(result.stderr)

    output.append(f"=== le code: {result.returncode} ===") #code indique est ce que le code  la gravite de code 

    return "\n".join(output)
>>>>>>> d9fe5f2dafd293d551733b3601d1483f99afa631
