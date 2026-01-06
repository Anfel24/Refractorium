import json
import os
import time



def read_file(path):
if not path.startswith("sandbox"):
    raise PermissionError("Accès interdit hors sandbox")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
     if not path.startswith("sandbox"):
        raise PermissionError("Accès interdit hors sandbox")
    with open(path, "w", encoding="utf-8") as f:

        f.write(content)

 

def save_files_to_disk(target_dir: str, files_content: dict):
  
   # Écrit les fichiers du projet sur le disque.

   
 

  
    os.makedirs(target_dir, exist_ok=True)

    # Parcourir tous les fichiers a ecrire
    for file_path, content in files_content.items():
        # Construire le chemin complet du fichier
        full_path = os.path.join(target_dir, file_path)

      
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Écrire le contenu dans le fichier
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
