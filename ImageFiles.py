# -*- coding: utf-8 -*-
"""
ImageFiles.py : ** REQUIRED ** El vostre codi de la classe ImageFiles.

Aquesta classe s'encarrega de gestionar el llistat d'arxius PNG dins la col·lecció d'imatges.

Funcionalitat:
    - Recórrer el filesystem a partir de ROOT_DIR per trobar tots els arxius PNG
    - Mantenir una representació en memòria dels arxius presents
    - Detectar quins arxius s'han afegit o eliminat des de l'última lectura

Mètodes a implementar:
    - reload_fs(path: str) -> None
        Recorre el directori especificat i actualitza la llista d'arxius PNG.
        Detecta els arxius nous i els que s'han eliminat.

    - files_added() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han afegit des de l'última crida a reload_fs().

    - files_removed() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han eliminat des de l'última crida a reload_fs().

Notes:
    - Els paths han de ser sempre relatius a ROOT_DIR
    - Només considereu arxius amb extensió .png (case-insensitive)
    - Heu de recórrer tots els subdirectoris recursivament
"""

import cfg
import os

class ImageFiles:
    def __init__(self):
        self.current_files = set()
        self.added_files = set()
        self.removed_files = set()

    def reload_fs(self, path: str) -> None:
        
        if not os.path.isdir(path):
            self.removed_files = self.current_files.copy()
            self.current_files = set()
            self.added_files = set()
            return

        previous_files = self.current_files.copy()
        new_files = set()
        
        for root_dir, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith('.png'):
                    full_path = os.path.join(root_dir, file)
                    new_files.add(full_path)
        
        self.added_files = new_files - previous_files
        self.removed_files = previous_files - new_files
        self.current_files = new_files

    def files_added(self): 
        return list(self.added_files)
        
    def files_removed(self): 
        return list(self.removed_files)
        
    def __len__(self): 
        return len(self.current_files)
        
    def __str__(self):
        return f"ImageFiles: {len(self)} fitxers (+{len(self.added_files)} afegits, -{len(self.removed_files)} eliminats)"