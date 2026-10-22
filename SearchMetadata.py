# -*- coding: utf-8 -*-
import cfg
import re


class SearchMetadata:
    def __init__(self, data):
        self.data = data

        self._index = {
            "prompt": {},
            "model": {},
            "seed": {},
            "cfg_scale": {},
            "steps": {},
            "sampler": {},
            "date": {}
        }

        self._all_uuids = set()
        self._preprocess()

    def _preprocess(self):

        if hasattr(self.data, 'images_data') and isinstance(self.data.images_data, dict):
            uuids = self.data.images_data.keys()
        elif hasattr(self.data, 'get_all_uuids'):
            uuids = self.data.get_all_uuids()
        else:
            return

        for uuid in uuids:
            self._all_uuids.add(uuid)

            self._add_to_index("prompt", uuid, self.data.get_prompt(uuid))
            self._add_to_index("model", uuid, self.data.get_model(uuid))
            self._add_to_index("seed", uuid, self.data.get_seed(uuid))
            self._add_to_index("cfg_scale", uuid, self.data.get_cfg_scale(uuid))
            self._add_to_index("steps", uuid, self.data.get_steps(uuid))
            self._add_to_index("sampler", uuid, self.data.get_sampler(uuid))
            self._add_to_index("date", uuid, self.data.get_created_date(uuid))

    def _add_to_index(self, field, uuid, value):

        if value is None:
            return

        text = str(value).lower()
        tokens = re.findall(r"\w+", text)

        field_index = self._index[field]

        for token in tokens:
            if token not in field_index:
                field_index[token] = set()
            field_index[token].add(uuid)

    def _search(self, sub, field):

        if not sub:
            return []

        tokens = re.findall(r"\w+", str(sub).lower())
        if not tokens:
            return []

        field_index = self._index[field]

        result = None
        for token in tokens:
            uuids = field_index.get(token, set())
            if result is None:
                result = set(uuids)
            else:
                result &= uuids

            if not result:
                break

        return list(result) if result else []

    def prompt(self, sub):
        return self._search(sub, "prompt")

    def model(self, sub):
        return self._search(sub, "model")

    def seed(self, sub):
        return self._search(sub, "seed")

    def cfg_scale(self, sub):
        return self._search(sub, "cfg_scale")

    def steps(self, sub):
        return self._search(sub, "steps")

    def sampler(self, sub):
        return self._search(sub, "sampler")

    def date(self, sub):
        return self._search(sub, "date")

    def and_operator(self, list1, list2):
        return list(set(list1) & set(list2))

    def or_operator(self, list1, list2):
        return list(set(list1) | set(list2))

    def __len__(self):
        return len(self._all_uuids)

    def __str__(self):
        return "SearchMetadata"
