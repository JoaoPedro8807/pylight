import hashlib
import json
from typing import Any


class PylightCache:
    def __init__(self, max_size: int = 1000):
        from .lru.lru import LRUCache
        self.cache = LRUCache(max_size)

    def make_query_key(self, model_name: str, filter_dict: dict):
        sorted_filters = json.dumps(filter_dict, sort_keys=True) #make string and sort it
        raw_key = f"{model_name}:{sorted_filters}"
        hashed_key = hashlib.md5(raw_key.encode()).hexdigest() 
        return f"query:{model_name}:{hashed_key}"

    def get(self, model_name: str, filter_dict: dict):
        key = self.make_query_key(model_name, filter_dict)
        return self.cache.get(key)

    def set(self, model_name: str, filter_dict: dict, value: Any):
        key = self.make_query_key(model_name, filter_dict)
        self.cache.set(key, value)