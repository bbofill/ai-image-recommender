# -*- coding: utf-8 -*-
"""
ImageData.py : ** REQUIRED ** El vostre codi de la classe ImageData.

Aquesta classe s'encarrega d'emmagatzemar i gestionar les metadades de les
imatges generades per IA.

Funcionalitat:
    - Afegir i eliminar imatges de la col·lecció
    - Llegir les metadades embegudes dins els arxius PNG
    - Proporcionar accés a totes les metadades d'una imatge

Mètodes a implementar:
    - add_image(uuid: str, file: str) -> None
        Crea una entrada per a la imatge amb l'UUID i el path especificats.
        Inicialment les metadades estan buides (no llegides del disc).

    - remove_image(uuid: str) -> None
        Elimina la imatge i totes les seves metadades de la col·lecció.

    - load_metadata(uuid: str) -> None
        Llegeix les metadades embegudes en l'arxiu PNG i les emmagatzema.
        Aquest mètode es pot cridar múltiples vegades (p.ex. si l'arxiu canvia).

    - get_prompt(uuid: str) -> str
        Retorna el prompt utilitzat per generar la imatge.

    - get_model(uuid: str) -> str
        Retorna el model d'IA utilitzat (p.ex. "SD2", "DALL-E", "Midjourney").

    - get_seed(uuid: str) -> str
        Retorna la llavor aleatòria utilitzada en la generació.

    - get_cfg_scale(uuid: str) -> str
        Retorna el CFG Scale (guidance scale) utilitzat.

    - get_steps(uuid: str) -> str
        Retorna el nombre de passos d'iteració del model.

    - get_sampler(uuid: str) -> str
        Retorna l'algorisme de mostreig utilitzat.

    - get_generated(uuid: str) -> str
        Retorna "true" si la imatge està marcada com a generada.

    - get_created_date(uuid: str) -> str
        Retorna la data de creació en format YYYY-MM-DD.

    - get_dimensions(uuid: str) -> tuple
        Retorna una tupla (width, height) amb les dimensions de la imatge.

Notes:
    - Utilitzeu la llibreria PIL/Pillow per llegir metadades:
      img = Image.open(file)
      metadata = img.text
    - Si un camp no existeix, retorneu "None" (string)
    - Les dimensions es llegeixen amb img.width i img.height
    - Tots els camps de metadades es guarden com a strings
"""

import cfg 
import os
from PIL import Image

class ImageData:

    def __init__(self):
        self.images_data = {}

    def add_image(self, uuid, file):
        self.images_data[uuid] = {
            "file_path": file,
            "Prompt": None,
            "Model": None,
            "Seed": None,
            "CFG_Scale": None,
            "Steps": None,
            "Sampler": None,
            "Generated": None,
            "Created_Date": None,
            "dimensions": (None, None)
        }

    def remove_image(self, uuid):
        self.images_data.pop(uuid, None)

    def load_metadata(self, uuid):
        if uuid not in self.images_data:
            return
        
        entry = self.images_data[uuid]
        relative_path = entry['file_path']
        full_path = os.path.join(cfg.get_root(), relative_path)
        
        if not os.path.isfile(full_path):
            return
            
        data = cfg.read_png_metadata(full_path)
        if not data:
            data = {}

        with Image.open(full_path) as img:
            dims = (img.width, img.height)

        entry["Prompt"] = data.get("Prompt", "")
        entry["Model"] = data.get("Model", "")
        entry["Seed"] = data.get("Seed", "")
        entry["CFG_Scale"] = data.get("CFG_Scale", "")
        entry["Steps"] = data.get("Steps", "")
        entry["Sampler"] = data.get("Sampler", "")
        entry["Generated"] = data.get("Generated", "")
        entry["Created_Date"] = data.get("Created_Date", "")
        entry["dimensions"] = dims
    
    def _get_field(self, uuid: str, field_name: str, default_value=None):
        entry = self.images_data.get(uuid, {})
        return entry.get(field_name, default_value)

    def get_prompt(self, uuid: str):
        return self._get_field(uuid, 'Prompt', None)

    def get_model(self, uuid: str):
        return self._get_field(uuid, 'Model', None)

    def get_seed(self, uuid: str):
        return self._get_field(uuid, 'Seed', None)

    def get_cfg_scale(self, uuid: str):
        return self._get_field(uuid, 'CFG_Scale', None)

    def get_steps(self, uuid: str):
        return self._get_field(uuid, 'Steps', None)

    def get_sampler(self, uuid: str):
        return self._get_field(uuid, 'Sampler', None)

    def get_generated(self, uuid: str):
        return self._get_field(uuid, 'Generated', None)

    def get_created_date(self, uuid: str):
        return self._get_field(uuid, 'Created_Date', None)

    def get_dimensions(self, uuid: str):
        return self._get_field(uuid, 'dimensions', (None, None))
    
    def get_file_path(self, uuid: str):
        return self._get_field(uuid, 'file_path', None)

    def get_all_uuids(self):
        return list(self.images_data.keys())

    def __len__(self) -> int:
        return len(self.images_data)

    def __str__(self) -> str:
        return f"ImageData (Gestionant {len(self)} imatges)"