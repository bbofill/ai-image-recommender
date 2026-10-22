# -*- coding: utf-8 -*-
"""
Gallery.py : ** REQUIRED ** El vostre codi de la classe Gallery.

Aquesta classe s'encarrega de gestionar galeries d'imatges en format JSON.

Funcionalitat:
    - Llegir galeries des d'arxius JSON
    - Visualitzar totes les imatges d'una galeria
    - Afegir i eliminar imatges de la galeria

Format JSON d'una galeria:
{
  "gallery_name": "Cyberpunk Cities",
  "description": "Collection of futuristic urban landscapes",
  "created_date": "2025-09-30",
  "images": [
    "generated_images/city_001.png",
    "generated_images/city_neon_12.png",
    "generated_images/urban_street_45.png"
  ]
}

Mètodes a implementar:
    - load_file(file: str) -> None
        Llegeix un arxiu JSON amb la definició de la galeria.
        Ha de validar que cada imatge referenciada existeix a la col·lecció.
        Si una imatge no existeix, l'ignora i continua processant.
        Emmagatzema internament els UUID de les imatges vàlides.

    - show() -> None
        Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image().

    - add_image_at_end(uuid: str) -> None
        Afegeix una imatge al final de la galeria.

    - remove_first_image() -> None
        Elimina la primera imatge de la galeria.

    - remove_last_image() -> None
        Elimina l'última imatge de la galeria.

Notes:
    - Utilitzeu la llibreria json per llegir els arxius
    - Els paths dins el JSON són relatius a ROOT_DIR
    - Cada galeria és un objecte independent (instància de Gallery)
    - Podeu tenir múltiples galeries actives simultàniament
    - Les operacions d'afegir/eliminar són ràpides (no busquen a la llista)
"""


import cfg 
import json    
import os

class Gallery:

    def __init__(self, image_id_manager=None, viewer=None):
        self.id_manager = image_id_manager
        self.viewer = viewer
        self.gallery_name = ""
        self.description = ""
        self.created_date = ""
        self.images = []

    def load_file(self, file):
        self.images = []
        if not os.path.isfile(file):
            return

        with open(file, 'r') as f:
            data = json.load(f)
            
        self.gallery_name = data.get("gallery_name", "")
        self.description = data.get("description", "")
        self.created_date = data.get("created_date", "")
        
        image_paths = data.get('images', [])
        
        for path in image_paths:
            path_ok = cfg.get_canonical_pathfile(path)
            uuid = self.id_manager.get_uuid(path_ok)
            if uuid:
                self.images.append(uuid)

    def show(self):
        for uuid in self.images:
            self.viewer.show_image(uuid, cfg.DISPLAY_MODE)

    def add_image_at_end(self, uuid):
        self.images.append(uuid)

    def remove_first_image(self):
        if self.images:
            self.images.pop(0)

    def remove_last_image(self):
        if self.images:
            self.images.pop()

    def __len__(self):
        return len(self.images)

    def __str__(self):
        return f"Gallery (Nom: '{self.gallery_name}', Imatges: {len(self.images)})"