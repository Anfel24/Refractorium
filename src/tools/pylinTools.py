
    import subprocess

def runpylint(target_dir: str) -> str:
    result = subprocess.run(
        ["pylint", target_dir],
        capture_output=True,
        text=True
    )

    output = []

    if result.stdout:
        output.append("=== pylint output ===")
        output.append(result.stdout)

    if result.stderr:
        output.append("=== pylint errors ===")
        output.append(result.stderr)

    output.append(f" return code: {result.returncode} ===") #code indique est ce que le code  la gravite de code 

    return "\n".join(output)

