import json
import heapq
from array import array
from Gallery import Gallery


class RecommenderSystem:

    def __init__(self, vectors_path: str, image_data=None, image_id=None):
        self.vectors_path = vectors_path
        self._image_data = image_data
        self._image_id = image_id
        self._flat_array = array('f')
        self._uuids = []
        self._uuid_to_idx = {}
        self._dim = 0
        self._sim_cache = {}     

    def preprocess(self):

        with open(self.vectors_path, 'r') as f:
            data = json.load(f)
            vectors_dict = data.get("vectors", data)

        temp_vals = []
        self._uuids = []
        self._uuid_to_idx = {}

        for idx, (uuid, content) in enumerate(vectors_dict.items()):

            vec = content.get('image_embedding')
            if not vec:
                continue

            norm = sum(x * x for x in vec) ** 0.5
            if norm > 0:
                vec = [x / norm for x in vec]

            temp_vals.extend(vec)
            self._uuids.append(uuid)
            self._uuid_to_idx[uuid] = idx
            self._dim = len(vec)

        self._flat_array = array('f', temp_vals)

    def find_similar_images(self, query_uuid: str, k: int = 10) -> Gallery:

        gallery = Gallery(self._image_id)
        q_id = query_uuid

        if q_id in self._sim_cache:
            gallery.images = self._sim_cache[q_id][:k]
            return gallery

        q_idx = self._uuid_to_idx.get(q_id)
        if q_idx is None:
            return gallery

        dim = self._dim
        q_start = q_idx * dim
        q_vec = self._flat_array[q_start:q_start + dim]

        flat = self._flat_array
        uuids = self._uuids
        num_imgs = len(uuids)

        TOP_N = 100 
        heap = []

        h_push = heapq.heappush
        h_replace = heapq.heapreplace
        indices = range(dim)

        for i in range(num_imgs):
            if i == q_idx:
                continue

            offset = i * dim
            sim = 0.0

            for j in indices:
                sim += q_vec[j] * flat[offset + j]

            if len(heap) < TOP_N:
                h_push(heap, (sim, uuids[i]))
            elif sim > heap[0][0]:
                h_replace(heap, (sim, uuids[i]))

        res = [item[1] for item in sorted(heap, reverse=True)]

        self._sim_cache[q_id] = res

        gallery.images = res[:k]
        return gallery

    def find_transition_prompts(self, uuid_1: str, uuid_2: str) -> list:
        return []
