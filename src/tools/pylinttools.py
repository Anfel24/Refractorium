import subprocess

def runpylint(target_dir):
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

