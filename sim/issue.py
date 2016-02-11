

class Issue:
    def __init__(self, name, candidates):
        self._name = name
        self._candidates = candidates

    @property
    def candidates(self):
        return self._candidates