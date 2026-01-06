
import json
import os
import time


<<<<<<< HEAD
def read_file(path):
=======

 def read_file(path):
>>>>>>> 87d325640bc6a2c45a85a17a084f57d8d48bcce8
    if not path.startswith("sandbox"):
        raise PermissionError("Accès interdit hors sandbox")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


<<<<<<< HEAD
def write_file(path, content):
=======
 def write_file(path, content):
>>>>>>> 87d325640bc6a2c45a85a17a084f57d8d48bcce8
    if not path.startswith("sandbox"):
        raise PermissionError("Accès interdit hors sandbox")

    with open(path, "w", encoding="utf-8") as f:
<<<<<<< HEAD
        f.write(content) 
=======
        f.write(content)
>>>>>>> 87d325640bc6a2c45a85a17a084f57d8d48bcce8
