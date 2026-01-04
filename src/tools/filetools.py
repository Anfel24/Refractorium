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
