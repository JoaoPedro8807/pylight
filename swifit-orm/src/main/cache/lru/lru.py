from collections import OrderedDict


class LRUCache:
    def __init__(self, max_size: int):
        self.cache = OrderedDict()  # Armazenamento do cache
        self.max_size = max_size

    def get(self, key):
        # Verifica se a chave está no cache
        if key not in self.cache:
            return None
        # Move o item para o final (mais recentemente usado)
        self.cache.move_to_end(key)

        return self.cache[key]

    def set(self, key, value):
        # Se a chave já existir, mova para o final
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.max_size: #verificar se vai se por mb ou por item
            self.cache.popitem(last=False)              # Se o cache estiver cheio, remove o item mais antigo (primeiro)
        self.cache[key] = value        # Adiciona ou atualiza o valor

